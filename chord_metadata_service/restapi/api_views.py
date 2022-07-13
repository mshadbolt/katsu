import math
import logging

from collections import Counter
from typing import TypedDict, Mapping
from calendar import month_abbr

from django.conf import settings
from django.views.decorators.cache import cache_page
from django.db.models import Count, F, Func, CharField, IntegerField, Case, When, Value
from django.db.models.functions import Cast, Substr
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from chord_metadata_service.restapi.utils import parse_individual_age
from chord_metadata_service.chord.permissions import OverrideOrSuperUserOnly
from chord_metadata_service.metadata.service_info import SERVICE_INFO
from chord_metadata_service.chord import models as chord_models
from chord_metadata_service.phenopackets import models as pheno_models
from chord_metadata_service.mcode import models as mcode_models
from chord_metadata_service.patients import models as patients_models
from chord_metadata_service.experiments import models as experiments_models
from chord_metadata_service.mcode.api_views import MCODEPACKET_PREFETCH, MCODEPACKET_SELECT


logger = logging.getLogger("restapi_api_views")
logger.setLevel(logging.INFO)

OVERVIEW_AGE_BIN_SIZE = 10


class BinnedStats(TypedDict):
    labels: list[str]
    values: list[int]


@api_view()
@permission_classes([AllowAny])
def service_info(_request):
    """
    get:
    Return service info
    """

    return Response(SERVICE_INFO)


# Cache page for the requested url for 2 hours
@cache_page(60 * 60 * 2)
@api_view(["GET"])
@permission_classes([OverrideOrSuperUserOnly])
def overview(_request):
    """
    get:
    Overview of all Phenopackets in the database
    """
    phenopackets_count = pheno_models.Phenopacket.objects.all().count()
    biosamples_count = pheno_models.Biosample.objects.all().count()
    individuals_count = patients_models.Individual.objects.all().count()
    experiments_count = experiments_models.Experiment.objects.all().count()
    experiment_results_count = experiments_models.ExperimentResult.objects.all().count()
    instruments_count = experiments_models.Instrument.objects.all().count()
    phenotypic_features_count = pheno_models.PhenotypicFeature.objects.all().distinct('pftype').count()

    # Sex related fields stats are precomputed here and post processed later
    # to include missing values inferred from the schema
    individuals_sex = stats_for_field(patients_models.Individual, "sex")
    individuals_k_sex = stats_for_field(patients_models.Individual, "karyotypic_sex")

    diseases_stats = stats_for_field(pheno_models.Phenopacket, "diseases__term__label")
    diseases_count = len(diseases_stats)

    # age_numeric is computed at ingestion time of phenopackets. On some instances
    # it might be unavailable and as a fallback must be computed from the age JSON field which
    # has two alternate formats (hence more complex and slower to process)
    individuals_age = get_field_bins(patients_models.Individual, "age_numeric", OVERVIEW_AGE_BIN_SIZE)
    if None in individuals_age:  # fallback
        del individuals_age[None]
        individuals_age = Counter(individuals_age)
        individuals_age.update(
            compute_binned_ages(OVERVIEW_AGE_BIN_SIZE)   # single update instead of creating iterables in a loop
        )

    r = {
        "phenopackets": phenopackets_count,
        "data_type_specific": {
            "biosamples": {
                "count": biosamples_count,
                "taxonomy": stats_for_field(pheno_models.Biosample, "taxonomy__label"),
                "sampled_tissue": stats_for_field(pheno_models.Biosample, "sampled_tissue__label"),
            },
            "diseases": {
                # count is a number of unique disease terms (not all diseases in the database)
                "count": diseases_count,
                "term": diseases_stats
            },
            "individuals": {
                "count": individuals_count,
                "sex": {k: individuals_sex.get(k, 0) for k in (s[0] for s in pheno_models.Individual.SEX)},
                "karyotypic_sex": {
                    k: individuals_k_sex.get(k, 0) for k in (s[0] for s in pheno_models.Individual.KARYOTYPIC_SEX)
                },
                "taxonomy": stats_for_field(patients_models.Individual, "taxonomy__label"),
                "age": individuals_age,
                "ethnicity": stats_for_field(patients_models.Individual, "ethnicity"),
            },
            "phenotypic_features": {
                # count is a number of unique phenotypic feature types (not all pfs in the database)
                "count": phenotypic_features_count,
                "type": stats_for_field(pheno_models.PhenotypicFeature, "pftype__label")
            },
            "experiments": {
                "count": experiments_count,
                "study_type": stats_for_field(experiments_models.Experiment, "study_type"),
                "experiment_type": stats_for_field(experiments_models.Experiment, "experiment_type"),
                "molecule": stats_for_field(experiments_models.Experiment, "molecule"),
                "library_strategy": stats_for_field(experiments_models.Experiment, "library_strategy"),
                "library_source": stats_for_field(experiments_models.Experiment, "library_source"),
                "library_selection": stats_for_field(experiments_models.Experiment, "library_selection"),
                "library_layout": stats_for_field(experiments_models.Experiment, "library_layout"),
                "extraction_protocol": stats_for_field(experiments_models.Experiment, "extraction_protocol"),
            },
            "experiment_results": {
                "count": experiment_results_count,
                "file_format": stats_for_field(experiments_models.ExperimentResult, "file_format"),
                "data_output_type": stats_for_field(experiments_models.ExperimentResult, "data_output_type"),
                "usage": stats_for_field(experiments_models.ExperimentResult, "usage")
            },
            "instruments": {
                "count": instruments_count,
                "platform": stats_for_field(experiments_models.Experiment, "instrument__platform"),
                "model": stats_for_field(experiments_models.Experiment, "instrument__model")
            },
        }
    }

    return Response(r)


# Cache page for the requested url for 2 hours
@cache_page(60 * 60 * 2)
@api_view(["GET"])
@permission_classes([OverrideOrSuperUserOnly])
def mcode_overview(_request):
    """
    get:
    Overview of all mCode data in the database
    """
    mcodepackets = mcode_models.MCodePacket.objects.all()\
        .prefetch_related(*MCODEPACKET_PREFETCH)\
        .select_related(*MCODEPACKET_SELECT)

    # cancer condition code
    cancer_condition_counter = Counter()
    # cancer related procedure type - radiation vs. surgical
    cancer_related_procedure_type_counter = Counter()
    # cancer related procedure code
    cancer_related_procedure_counter = Counter()
    # cancer disease status
    cancer_disease_status_counter = Counter()

    individuals_set = set()
    individuals_sex = Counter()
    individuals_k_sex = Counter()
    individuals_taxonomy = Counter()
    individuals_age = Counter()
    individuals_ethnicity = Counter()

    for mcodepacket in mcodepackets:
        # subject/individual
        individual = mcodepacket.subject
        individuals_set.add(individual.id)
        individuals_sex.update((individual.sex,))
        individuals_k_sex.update((individual.karyotypic_sex,))
        if individual.ethnicity != "":
            individuals_ethnicity.update((individual.ethnicity,))
        if individual.age is not None:
            individuals_age.update((parse_individual_age(individual.age),))
        if individual.taxonomy is not None:
            individuals_taxonomy.update((individual.taxonomy["label"],))
        for cancer_condition in mcodepacket.cancer_condition.all():
            cancer_condition_counter.update((cancer_condition.code["label"],))
        for cancer_related_procedure in mcodepacket.cancer_related_procedures.all():
            cancer_related_procedure_type_counter.update((cancer_related_procedure.procedure_type,))
            cancer_related_procedure_counter.update((cancer_related_procedure.code["label"],))
        if mcodepacket.cancer_disease_status is not None:
            cancer_disease_status_counter.update((mcodepacket.cancer_disease_status["label"],))

    return Response({
        "mcodepackets": mcodepackets.count(),
        "data_type_specific": {
            "cancer_conditions": {
                "count": len(cancer_condition_counter.keys()),
                "term": dict(cancer_condition_counter)
            },
            "cancer_related_procedure_types": {
                "count": len(cancer_related_procedure_type_counter.keys()),
                "term": dict(cancer_related_procedure_type_counter)
            },
            "cancer_related_procedures": {
                "count": len(cancer_related_procedure_counter.keys()),
                "term": dict(cancer_related_procedure_counter)
            },
            "cancer_disease_status": {
                "count": len(cancer_disease_status_counter.keys()),
                "term": dict(cancer_disease_status_counter)
            },
            "individuals": {
                "count": len(individuals_set),
                "sex": {k: individuals_sex[k] for k in (s[0] for s in pheno_models.Individual.SEX)},
                "karyotypic_sex": {
                    k: individuals_k_sex[k] for k in (s[0] for s in pheno_models.Individual.KARYOTYPIC_SEX)
                },
                "taxonomy": dict(individuals_taxonomy),
                "age": dict(individuals_age),
                "ethnicity": dict(individuals_ethnicity)
            },
        }
    })


@api_view(["GET"])
@permission_classes([AllowAny])
def public_search_fields(_request):
    """
    get:
    Return public search fields with their configuration
    """
    if settings.CONFIG_PUBLIC:
        search_conf = settings.CONFIG_PUBLIC["search"]
        field_conf = settings.CONFIG_PUBLIC["fields"]
        r = [
            {
                **section,
                "fields": [field_conf[f] for f in section["fields"]]
            } for section in search_conf
        ]
        return Response(r)
    else:
        return Response(settings.NO_PUBLIC_FIELDS_CONFIGURED)


@api_view(["GET"])
@permission_classes([AllowAny])
def public_overview(_request):
    """
    get:
    Overview of all public data in the database
    """

    # TODO should this be added to the project config.json file ?
    threshold = 5
    missing = "missing"

    if settings.CONFIG_FIELDS:

        # Datasets provenance metadata
        datasets = chord_models.Dataset.objects.values(
            "title", "description", "contact_info",
            "dates", "stored_in", "spatial_coverage",
            "types", "privacy", "distributions",
            "dimensions", "primary_publications", "citations",
            "produced_by", "creators", "licenses",
            "acknowledges", "keywords", "version",
            "extra_properties"
        )

        individuals = patients_models.Individual.objects.all()
        individuals_set = set()
        individuals_sex = Counter()
        individuals_age = Counter()
        individuals_extra_properties = {}
        extra_properties = {}

        experiments = experiments_models.Experiment.objects.all()
        experiments_set = set()
        experiments_type = Counter()

        for individual in individuals:
            # subject/individual
            individuals_set.add(individual.id)
            individuals_sex.update((individual.sex,))
            # age
            if individual.age is not None:
                individuals_age.update((parse_individual_age(individual.age),))
            # collect extra_properties defined in config
            if individual.extra_properties and "extra_properties" in settings.CONFIG_FIELDS:
                for key in individual.extra_properties:
                    if key in settings.CONFIG_FIELDS["extra_properties"]:
                        # add new Counter()
                        if key not in extra_properties:
                            extra_properties[key] = Counter()
                        try:
                            extra_properties[key].update((individual.extra_properties[key],))
                        except TypeError:
                            logger.error(f"The extra_properties {key} value is not of type string or number.")
                            pass

                        individuals_extra_properties[key] = dict(extra_properties[key])
        # Experiments
        for experiment in experiments:
            experiments_set.add(experiment.id)
            experiments_type.update((experiment.experiment_type,))

        # Put age in bins
        if individuals_age:
            age_bin_size = settings.CONFIG_FIELDS["age"]["bin_size"] \
                if "age" in settings.CONFIG_FIELDS and "bin_size" in settings.CONFIG_FIELDS["age"] else None
            age_kwargs = dict(values=dict(individuals_age), bin_size=age_bin_size)
            individuals_age_bins = sort_numeric_values_into_bins(
                **{k: v for k, v in age_kwargs.items() if v is not None}
            )
        else:
            individuals_age_bins = {}

        # Put all other numeric values coming from extra_properties in bins and remove values where count <= threshold
        if individuals_extra_properties:
            for key, value in list(individuals_extra_properties.items()):
                # extra_properties contains only the fields specified in config
                if settings.CONFIG_FIELDS["extra_properties"][key]["type"] == "number":
                    # retrieve bin_size if available
                    field_bin_size = settings.CONFIG_FIELDS["extra_properties"][key]["bin_size"] \
                        if "bin_size" in settings.CONFIG_FIELDS["extra_properties"][key] else None
                    # retrieve the values from extra_properties counter
                    values = individuals_extra_properties[key]
                    if values:
                        kwargs = dict(values=values, bin_size=field_bin_size)
                        # sort into bins and remove numeric values where count <= threshold
                        extra_prop_values_in_bins = sort_numeric_values_into_bins(
                            **{k: v for k, v in kwargs.items() if v is not None}
                        )
                        # rewrite with sorted values
                        individuals_extra_properties[key] = extra_prop_values_in_bins
                    # add missing value count
                    individuals_extra_properties[key][missing] = len(individuals_set) - sum(v for v in value.values())
                else:
                    # add missing value count
                    value[missing] = len(individuals_set) - sum(v for v in value.values())
                    # remove string values where count <= threshold
                    for k, v in list(value.items()):
                        if v <= 5 and k != missing:
                            individuals_extra_properties[key].pop(k)

        # Update counters with missing values
        for counter, all_values in zip([individuals_sex, individuals_age_bins], [individuals_sex, individuals_age]):
            counter[missing] = len(individuals_set) - sum(v for v in dict(all_values).values())

        # Response content
        if len(individuals_set) < threshold:
            content = settings.INSUFFICIENT_DATA_AVAILABLE
        else:
            content = {
                "individuals": len(individuals_set)
            }
            for field, value in zip(
                    ["sex", "age", "extra_properties", "experiment_type"],
                    [{k: v for k, v in dict(individuals_sex).items() if v > threshold or k == missing},
                     individuals_age_bins,
                     individuals_extra_properties,
                     dict(experiments_type)]):
                if field in settings.CONFIG_FIELDS:
                    content[field] = value
            if "experiment_type" in content:
                content["experiments"] = len(experiments_set)
            content["datasets"] = datasets
        return Response(content)

    else:
        return Response(settings.NO_PUBLIC_DATA_AVAILABLE)


@api_view(["GET"])
@permission_classes([AllowAny])
def public_overview_new(_request):
    """
    get:
    Overview of all public data in the database
    """

    if not settings.CONFIG_PUBLIC:
        return Response(settings.NO_PUBLIC_DATA_AVAILABLE)

    # Datasets provenance metadata
    datasets = chord_models.Dataset.objects.values(
        "title", "description", "contact_info",
        "dates", "stored_in", "spatial_coverage",
        "types", "privacy", "distributions",
        "dimensions", "primary_publications", "citations",
        "produced_by", "creators", "licenses",
        "acknowledges", "keywords", "version",
        "extra_properties"
    )

    # Parse the public config to gather data for each field defined in the
    # overview

    fields = [field for section in settings.CONFIG_PUBLIC["overview"] for field in section["fields"]]
    response = {
        "datasets": datasets,
        "layout": settings.CONFIG_PUBLIC["overview"],
        "fields": {}
    }

    for field in fields:
        field_props = settings.CONFIG_PUBLIC["fields"][field]
        response["fields"][field] = {
            **field_props,
            "data": {}
        }
        if field_props["datatype"] == "string":
            stats = get_categorical_stats(field_props)
        elif field_props["datatype"] == "number":
            stats = get_range_stats(field_props)
        elif field_props["datatype"] == "date":
            stats = get_date_stats(field_props)

        response["fields"][field]["data"] = stats

    return Response(response)


def get_categorical_stats(field_props) -> BinnedStats:
    """
    Fetches statistics for a given categorical field and apply privacy policies
    """
    model, field_name = get_model_and_field(field_props["id"])
    stats = stats_for_field(model, field_name, add_missing=True)

    # Enforce values order from config and apply policies
    threshold = settings.CONFIG_PUBLIC["rules"]["count_threshold"]
    labels: list[str] = field_props["config"]["enum"]
    values: list[int] = []

    for category in labels:
        v = stats.get(category, 0)
        if v and v < threshold:
            v = 0
        values.append(v)

    if stats["missing"] > 0:
        labels.append("missing")
        values.append(stats["missing"])

    return {
        "labels": labels,
        "values": values
    }


def get_date_stats(field_props):
    """
    Fetches statistics for a given date field, fill the gaps in the date range
    and apply privacy policies.
    Note that dates within a JSON are stored as strings, not instances of datetime.
    TODO: for now, only dates in extra_properties are handled. Handle dates as
    regular fields when needed.
    TODO: for now only dates binned by month are handled
    """
    LENGTH_Y_M = 4 + 1 + 2  # dates stored as yyyy-mm-dd
    DATE_Y_M = 'date'
    threshold = settings.CONFIG_PUBLIC["rules"]["count_threshold"]

    if field_props["config"]["bin_by"] != "month":
        msg = f"Binning dates by `{field_props['config']['bin_by']}` method not implemented"
        logger.error(msg)
        raise NotImplementedError(msg)

    model, field_name = get_model_and_field(field_props["id"])

    if "extra_properties" not in field_name:
        msg = "Binning date-like fields that are not in extra-properties is not implemented"
        logger.error(msg)
        raise NotImplementedError(msg)

    query_set = model.objects.all()\
        .annotate(date=Substr(field_name, 1, LENGTH_Y_M))\
        .values(DATE_Y_M)\
        .annotate(total=Count(DATE_Y_M))\
        .order_by(DATE_Y_M)  # Note: lexical sort works on ISO dates

    stats: Mapping(str, int) = dict()
    has_missing = False
    for item in query_set:
        key = item[DATE_Y_M]
        if key is None:
            has_missing = True
            continue

        key = key.strip()
        if key == "":
            continue

        stats[key] = item["total"] if item["total"] > threshold else 0

    # All the bins between start and end date must be represented
    labels: list(str) = []
    values: list(int) = []
    if len(stats):
        keys = list(stats)
        for year, month in monthly_generator(keys[0], keys[-1]):
            key = f"{year}-{month}"
            label = f"{month_abbr[month].capitalize()} {year}"    # convert key as yyyy-mm to `abbreviated month yyyy`
            labels.append(label)
            values.appenf(stats.get(key, 0))

    # Append missing items if any
    if has_missing:
        isnull_filter = {f"{field_name}__isnull": True}
        v = model.objects.all().values(field_name).filter(**isnull_filter).count()
        labels.append("missing")
        values.append(v)

    return {
        "labels": labels,
        "values": values
    }


def get_range_stats(field_props):
    threshold = settings.CONFIG_PUBLIC["rules"]["count_threshold"]
    model, field = get_model_and_field(field_props["id"])

    # Generate a list of When conditions that return a label for the given bin.
    # This is equivalent to an SQL CASE statement.
    whens = [When(**{f"{field}__gte": floor},  **{f"{field}__lt": ceil}, then=Value(label))
             for floor, ceil, label in labelled_range_generator(field_props)]

    query_set = model.objects\
        .values(label=Case(*whens, default=Value("missing"), output_field=CharField()))\
        .annotate(total=Count("label"))

    stats: Mapping(str, int) = dict()
    for item in query_set:
        key = item["label"]
        stats[key] = item["total"] if item["total"] > threshold else 0

    # All the bins between start and end must be represented and ordered
    labels: list(str) = []
    values: list(int) = []
    for floor, ceil, label in labelled_range_generator(field_props):
        labels.append(label)
        values.append(stats.get(label, 0))

    if "missing" in stats:
        labels.append("missing")
        values.append(stats["missing"])

    return {
        "labels": labels,
        "values": values
    }


def labelled_range_generator(field_props) -> tuple(int, int, str):
    """
    Note: limited to operations on integer values for simplicity
    A word of caution: when implementing handling of floating point values,
    be aware of string format (might need to add precision to config?) computations
    of modulo and lack of support for ranges.
    """

    c = field_props["config"]
    minimum = int(c["minimum"])
    maximum = int(c["maximum"])
    taper_left = int(c["taper_left"])
    taper_right = int(c["taper_right"])
    bin_size = int(c["bin_size"])

    # check prerequisites
    # Note: it raises an error as it reflects an error in the config file
    if maximum < minimum:
        raise ValueError(f"Wrong min/max values in config: {field_props}")

    if (taper_right < taper_left
            or minimum > taper_left
            or taper_right > maximum):
        raise ValueError(f"Wrong taper values in config: {field_props}")

    if (taper_right - taper_left) % bin_size:
        raise ValueError(f"Range between taper values is not a multiple of bin_size: {field_props}")

    # start generator
    if minimum != taper_left:
        yield minimum, taper_left, f"{minimum}-{taper_left}"

    for v in range(taper_left, taper_right, bin_size):
        yield v, v + bin_size, f"{v}-{v + bin_size}"

    if maximum != taper_right:
        yield taper_right, maximum, f"≥ {taper_right}"


def monthly_generator(start: str, end: str) -> tuple(int, int):
    """
    generator of tuples (year nb, month nb) from a start date to an end date
    as ISO formated strings `yyyy-mm`
    """
    start_year, start_month = tuple([int(k) for k in start.split("-")])
    end_year, end_month = tuple([int(k) for k in end.split("-")])
    last_month_nb = (end_year - start_year) * 12 + end_month
    for month_nb in range(start_month, last_month_nb):
        year = start_year + month_nb // 12
        month = month_nb % 12
        yield year, month


def get_model_and_field(field_id: str) -> tuple(any, str):
    model_name, *field_path = field_id.split("/")

    if model_name == "individual":
        model = pheno_models.Individual
    elif model_name == "experiment":
        model = experiments_models.Experiment
    else:
        msg = f"Accessing field on model {model_name} not implemented"
        logger.error(msg)
        raise NotImplementedError(msg)

    field_name = "__".join(field_path)
    return model, field_name


def sort_numeric_values_into_bins(values: dict, bin_size: int = 10, threshold: int = 5):
    values_in_bins = {}
    # convert keys to int
    keys_to_int_values = {int(k): v for k, v in values.items()}
    # find the max value and define the  range
    for j in range(math.ceil(max(keys_to_int_values.keys()) / bin_size)):
        bin_key = j * bin_size
        keys = [a for a in keys_to_int_values.keys() if j * bin_size <= a < (j + 1) * bin_size]
        keys_sum = 0
        for k, v in keys_to_int_values.items():
            if k in keys:
                keys_sum += v
        values_in_bins[f"{bin_key}"] = keys_sum
    # remove data if count < 5
    return {k: v for k, v in values_in_bins.items() if v > threshold}


def stats_for_field(model, field: str, add_missing=False) -> Mapping(str, int):
    # values() restrict the table of results to this COLUMN
    # annotate() creates a `total` column for the aggregation
    # Count() aggregates the results by performing a GROUP BY on the field
    query_set = model.objects.all().values(field).annotate(total=Count(field))
    stats: Mapping(str, int) = dict()
    for item in query_set:
        key = item[field]
        if key is None:
            continue

        key = key.strip()
        if key == "":
            continue

        stats[key] = item["total"]

    if add_missing:
        isnull_filter = {f"{field}__isnull": True}
        stats['missing'] = model.objects.all().values(field).filter(**isnull_filter).count()

    return stats


def get_field_bins(model, field, bin_size):
    # creates a new field "binned" by substracting the modulo by bin size to
    # the value which requires binning (e.g. 28 => 28 - 28 % 10 = 20)
    # cast to integer to avoid numbers such as 60.00 if that was a decimal,
    # and aggregate over this value.
    query_set = model.objects.all().annotate(
        binned=Cast(
            F(field) - Func(F(field), bin_size, function="MOD"),
            IntegerField()
        )
    ).values('binned').annotate(total=Count('binned'))
    stats = {item['binned']: item['total'] for item in query_set}
    return stats


def compute_binned_ages(bin_size):
    a = pheno_models.Individual.objects.filter(age_numeric__isnull=True).values('age')
    binned_ages = []
    for r in a.iterator():  # reduce memory footprint (no caching)
        if r["age"] is None:
            continue
        age = parse_individual_age(r["age"])
        binned_ages.append(age - age % OVERVIEW_AGE_BIN_SIZE)
    return binned_ages
