"""
These lists contain the permissible values for their respective
MoH model fields and are used for validation during serialization.
"""

CAUSE_OF_DEATH = [
    "Died of cancer",
    "Died of other reasons",
    "Unknown",
]

PRIMARY_SITE = [
    "Accessory sinuses",
    "Adrenal gland",
    "Anus and anal canal",
    "Base of tongue",
    "Bladder",
    "Bones, joints and articular cartilage of limbs",
    "Bones, joints and articular cartilage of other and unspecified sites",
    "Brain",
    "Breast",
    "Bronchus and lung",
    "Cervix uteri",
    "Colon",
    "Connective, subcutaneous and other soft tissues",
    "Corpus uteri",
    "Esophagus",
    "Eye and adnexa",
    "Floor of mouth",
    "Gallbladder",
    "Gum",
    "Heart, mediastinum, and pleura",
    "Hematopoietic and reticuloendothelial systems",
    "Hypopharynx",
    "Kidney",
    "Larynx",
    "Lip",
    "Liver and intrahepatic bile ducts",
    "Lymph nodes",
    "Meninges",
    "Nasal cavity and middle ear",
    "Nasopharynx",
    "Oropharynx",
    "Other and ill-defined digestive organs",
    "Other and ill-defined sites",
    "Other and ill-defined sites in lip, oral cavity and pharynx",
    "Other and ill-defined sites within respiratory system and intrathoracic organs",
    "Other and unspecified female genital organs",
    "Other and unspecified major salivary glands",
    "Other and unspecified male genital organs",
    "Other and unspecified parts of biliary tract",
    "Other and unspecified parts of mouth",
    "Other and unspecified parts of tongue",
    "Other and unspecified urinary organs",
    "Other endocrine glands and related structures",
    "Ovary",
    "Palate",
    "Pancreas",
    "Parotid gland",
    "Penis",
    "Peripheral nerves and autonomic nervous system",
    "Placenta",
    "Prostate gland",
    "Pyriform sinus",
    "Rectosigmoid junction",
    "Rectum",
    "Renal pelvis",
    "Retroperitoneum and peritoneum",
    "Skin",
    "Small intestine",
    "Spinal cord, cranial nerves, and other parts of central nervous system",
    "Stomach",
    "Testis",
    "Thymus",
    "Thyroid gland",
    "Tonsil",
    "Trachea",
    "Unknown primary site",
    "Ureter",
    "Uterus, NOS",
    "Vagina",
    "Vulva",
]

TUMOUR_STAGING_SYSTEM = [
    "AJCC 8th edition",
    "AJCC 7th edition",
    "AJCC 6th edition",
    "Ann Arbor staging system",
    "Binet staging system",
    "Durie-Salmon staging system",
    "FIGO staging system",
    "Lugano staging system",
    "Rai staging system",
    "Revised International staging system (RISS)",
    "SEER staging system",
    "St Jude staging system",
]

T_CATEGORY = [
    "T0",
    "T1",
    "T1a",
    "T1a1",
    "T1a2",
    "T1a(s)",
    "T1a(m)",
    "T1b",
    "T1b1",
    "T1b2",
    "T1b(s)",
    "T1b(m)",
    "T1c",
    "T1d",
    "T1mi",
    "T2",
    "T2(s)",
    "T2(m)",
    "T2a",
    "T2a1",
    "T2a2",
    "T2b",
    "T2c",
    "T2d",
    "T3",
    "T3(s)",
    "T3(m)",
    "T3a",
    "T3b",
    "T3c",
    "T3d",
    "T3e",
    "T4",
    "T4a",
    "T4a(s)",
    "T4a(m)",
    "T4b",
    "T4b(s)",
    "T4b(m)",
    "T4c",
    "T4d",
    "T4e",
    "Ta",
    "Tis",
    "Tis(DCIS)",
    "Tis(LAMN)",
    "Tis(LCIS)",
    "Tis(Paget)",
    "Tis(Paget’s)",
    "Tis pu",
    "Tis pd",
    "TX"
]

N_CATEGORY = [
    "N0",
    "N0a",
    "N0a (biopsy)",
    "N0b",
    "N0b (no biopsy)",
    "N0(i+)",
    "N0(i-)",
    "N0(mol+)",
    "N0(mol-)",
    "N1",
    "N1a",
    "N1a(sn)",
    "N1b",
    "N1c",
    "N1mi",
    "N2",
    "N2a",
    "N2b",
    "N2c",
    "N2mi",
    "N3",
    "N3a",
    "N3b",
    "N3c",
    "N4",
    "NX"
]

M_CATEGORY = [
    "M0",
    "M0(i+)",
    "M1",
    "M1a",
    "M1a(0)",
    "M1a(1)",
    "M1b",
    "M1b(0)",
    "M1b(1)",
    "M1c",
    "M1c(0)",
    "M1c(1)",
    "M1d",
    "M1d(0)",
    "M1d(1)",
    "M1e",
    "MX"
]

STAGE_GROUP = [
    "Occult Carcinoma",
    "Stage 0",
    "Stage 0a",
    "Stage 0is",
    "Stage 1",
    "Stage 1A",
    "Stage 1B",
    "Stage A",
    "Stage B",
    "Stage C",
    "Stage I",
    "Stage IA",
    "Stage IA1",
    "Stage IA2",
    "Stage IA3",
    "Stage IAB",
    "Stage IAE",
    "Stage IAES",
    "Stage IAS",
    "Stage IB",
    "Stage IB1",
    "Stage IB2",
    "Stage IBE",
    "Stage IBES",
    "Stage IBS",
    "Stage IC",
    "Stage IE",
    "Stage IEA",
    "Stage IEB",
    "Stage IES",
    "Stage II",
    "Stage II bulky",
    "Stage IIA",
    "Stage IIA1",
    "Stage IIA2",
    "Stage IIAE",
    "Stage IIAES",
    "Stage IIAS",
    "Stage IIB",
    "Stage IIBE",
    "Stage IIBES",
    "Stage IIBS",
    "Stage IIC",
    "Stage IIE",
    "Stage IIEA",
    "Stage IIEB",
    "Stage IIES",
    "Stage III",
    "Stage IIIA",
    "Stage IIIA1",
    "Stage IIIA2",
    "Stage IIIAE",
    "Stage IIIAES",
    "Stage IIIAS",
    "Stage IIIB",
    "Stage IIIBE",
    "Stage IIIBES",
    "Stage IIIBS",
    "Stage IIIC",
    "Stage IIIC1",
    "Stage IIIC2",
    "Stage IIID",
    "Stage IIIE",
    "Stage IIIES",
    "Stage IIIS",
    "Stage IIS",
    "Stage IS",
    "Stage IV",
    "Stage IVA",
    "Stage IVA1",
    "Stage IVA2",
    "Stage IVAE",
    "Stage IVAES",
    "Stage IVAS",
    "Stage IVB",
    "Stage IVBE",
    "Stage IVBES",
    "Stage IVBS",
    "Stage IVC",
    "Stage IVE",
    "Stage IVES",
    "Stage IVS",
    "In situ",
    "Localized",
    "Regionalized",
    "Distant",
]

STORAGE = [
    "Cut slide",
    "Frozen in -70 freezer",
    "Frozen in liquid nitrogen",
    "Frozen in vapour phase",
    "Not Applicable",
    "Other",
    "Paraffin block",
    "RNA later frozen",
    "Unknown"
]

CONFIRMED_DIAGNOSIS_TUMOUR = [
    "Yes",
    "No",
    "Not done",
    "Unknown"
]

TUMOUR_GRADING_SYSTEM = [
    "FNCLCC grading system",
    "Four-tier grading system",
    "Gleason grade group system",
    "Grading system for GISTs",
    "Grading system for GNETs",
    "ISUP grading system",
    "Nuclear grading system for DCIS",
    "Scarff-Bloom-Richardson grading system",
    "Three-tier grading system",
    "Two-tier grading system",
    "WHO grading system for CNS tumours"
]

TUMOUR_GRADE = [
    "Low grade",
    "High grade",
    "GX",
    "G1",
    "G2",
    "G3",
    "G4",
    "Low",
    "High",
    "Grade I",
    "Grade II",
    "Grade III",
    "Grade IV",
    "Grade Group 1",
    "Grade Group 2",
    "Grade Group 3",
    "Grade Group 4",
    "Grade Group 5"
]

PERCENT_CELLS_RANGE = [
    "0-19%",
    "20-50%",
    "51-100%"
]

CELLS_MEASURE_METHOD = [
    "Genomics",
    "Image analysis",
    "Pathology estimate by percent nuclei",
    "Unknown"
]

GENDER = [
    "Man",
    "Woman",
    "Non-binary"
]

SEX_AT_BIRTH = [
    "Male",
    "Female",
    "Other",
    "Unknown"
]

SPECIMEN_TISSUE_SOURCE = [
    "Amniotic fluid",
    "Bile Fluid",
    "Whole blood",
    "Blood arterial",
    "Cord blood",
    "Blood venous",
    "Bone",
    "Serum, Convalescent",
    "Cerebral spinal fluid",
    "Cervical Mucus",
    "Duodenal fluid",
    "Blood, Fetal",
    "Fluid, Abdomen",
    "Genital vaginal",
    "Fluid, Hydrocele",
    "Fluid, Joint",
    "Fluid, Kidney",
    "Fluid, Lumbar Sac",
    "Marrow",
    "Pancreatic fluid",
    "Fluid, Pericardial",
    "Placenta",
    "Pleural fluid (thoracentesis fluid)",
    "Saliva",
    "Skin",
    "Seminal fluid",
    "Fluid, synovial (Joint fluid)",
    "Sputum",
    "Tissue",
    "Vitreous Fluid",
    "Wound"
]

SPECIMEN_TYPE = [
    "Cell line - derived from normal",
    "Cell line - derived from metastatic tumour",
    "Cell line - derived from primary tumour",
    "Cell line - derived from xenograft tumour",
    "Metastatic tumour - additional metastatic",
    "Metastatic tumour - metastasis local to lymph node",
    "Metastatic tumour - metastasis to distant location",
    "Metastatic tumour",
    "Normal - tissue adjacent to primary tumour",
    "Normal",
    "Primary tumour - additional new primary",
    "Primary tumour - adjacent to normal",
    "Primary tumour",
    "Recurrent tumour",
    "Xenograft - derived from primary tumour",
    "Xenograft - derived from metastatic tumour",
    "Xenograft - derived from tumour cell line",
]

SAMPLE_TYPE = [
    "Amplified DNA",
    "ctDNA",
    "Other DNA enrichments",
    "Other RNA fractions",
    "polyA+ RNA",
    "Protein",
    "rRNA-depleted RNA",
    "Total DNA",
    "Total RNA"
]

BASIS_OF_DIAGNOSIS = [
    "Clinical investigation",
    "Clinical",
    "Cytology",
    "Death certificate only",
    "Histology of a metastasis",
    "Histology of a primary tumour",
    "Specific tumour markers",
    "Unknown"
]

LYMPH_NODE_STATUS = [
    "Cannot be determined",
    "No",
    "No lymph nodes found in resected specimen",
    "Not applicable",
    "Yes"
]

LYMPH_NODE_METHOD = [
    "Imaging",
    "Lymph node dissection/pathological exam",
    "Physical palpation of patient"
]

TREATMENT_TYPE = [
    "Ablation",
    "Bone marrow transplant",
    "Chemotherapy",
    "Endoscopic therapy",
    "Hormonal therapy",
    "Immunotherapy",
    "No treatment",
    "Other targeting molecular therapy",
    "Photodynamic therapy",
    "Radiation therapy",
    "Stem cell transplant",
    "Surgery"
]

TREATMENT_SETTING = [
    "Adjuvant",
    "Advanced/Metastatic",
    "Neoadjuvant",
    "Not applicable"
]

TREATMENT_RESPONSE_METHOD = [
    "RECIST 1.1",
    "iRECIST",
    "Cheson CLL 2012 Oncology Response Criteria",
    "Response Assessment in Neuro-Oncology (RANO)",
    "AML Response Criteria",
    "Physician Assessed Response Criteria"
]

TREATMENT_RESPONSE = [
    "Complete response",
    "Partial response",
    "Progressive disease",
    "Stable disease",
    "Immune complete response (iCR)",
    "Immune partial response (iPR)",
    "Immune uncomfirmed progressive disease (iUPD)",
    "Immune confirmed progressive disease (iCPD)",
    "Immune stable disease (iSD)",
    "Complete remission",
    "Partial remission",
    "Minor response",
    "Complete remission without measurable residual disease (CR MRD-)",
    "Complete remission with incomplete hematologic recovery (CRi)",
    "Morphologic leukemia-free state",
    "Primary refractory disease",
    "Hematologic relapse (after CR MRD-, CR, CRi)",
    "Molecular relapse (after CR MRD-)",
    "Physician assessed complete response",
    "Physician assessed partial response",
    "Physician assessed stable disease",
    "No evidence of disease (NED)"
]

DOSAGE_UNITS = [
    "mg/m2",
    "IU/m2",
    "ug/m2",
    "g/m2",
    "mg/kg"
]

RADIATION_THERAPY_MODALITY = [
    "Megavoltage radiation therapy using photons (procedure)",
    "Teleradiotherapy using electrons (procedure)",
    "Teleradiotherapy protons (procedure)",
    "Teleradiotherapy neutrons (procedure)",
    "Brachytherapy (procedure)",
    "Other"
]

RADIATION_ANATOMICAL_SITE = [
    "Cervical lymph node group",
    "Entire lymph node of thorax",
    "Cervical lymph node group",
    "Entire lymph node of thorax",
    "Axillary lymph node group",
    "Supraclavicular lymph node group",
    "Internal mammary lymph node group",
    "Abdominal lymph node group",
    "Pelvic lymph node group",
    "Abdominal lymph node group",
    "Pelvic lymph node group",
    "Structure of lymph node",
    "Entire eye",
    "Pituitary structure",
    "Brain structure",
    "Brain part",
    "Spinal cord structure",
    "Nasopharyngeal structure",
    "Oral cavity structure",
    "Oropharyngeal structure",
    "Laryngeal structure",
    "Hypopharyngeal structure",
    "Nasal sinus structure",
    "Salivary gland structure",
    "Thyroid structure",
    "Entire head and neck",
    "Entire lung",
    "Mesothelium structure",
    "Entire thorax",
    "Entire breast",
    "Breast part",
    "Chest wall structure",
    "Entire esophagus",
    "Stomach structure",
    "Small intestinal structure",
    "Colon structure",
    "Rectum structure",
    "Anal structure",
    "Liver structure",
    "Biliary tract structure",
    "Gallbladder structure",
    "Pancreatic structure",
    "Abdominal structure",
    "Entire urinary bladder",
    "Bladder part",
    "Kidney structure",
    "Ureteric structure",
    "Entire prostate",
    "Prostate part",
    "Urethral structure",
    "Penile structure",
    "Testis structure",
    "Scrotal structure",
    "Ovarian structure",
    "Fallopian tube structure",
    "Uterine structure",
    "Cervix uteri structure",
    "Vaginal structure",
    "Vulval structure",
    "Bone structure of cranium",
    "Entire vertebral column",
    "Shoulder region structure",
    "Bone structure of rib",
    "Hip region structure",
    "Entire bony pelvis",
    "Pelvic structure",
    "Bone structure of extremity",
    "Skin structure",
    "Soft tissues",
    "Entire body as a whole"
]

IMMUNOTHERAPY_TYPE = [
    "Cell-based",
    "Immune checkpoint inhibitors",
    "Monoclonal antibodies other than immune checkpoint inhibitors",
    "Other immunomodulatory substances"
]

SURGERY_TYPE = [
    "Axillary Clearance",
    "Axillary lymph nodes sampling",
    "Biopsy",
    "Bypass Gastrojejunostomy",
    "Cholecystectomy",
    "Cholecystojejunostomy",
    "Completion gastrectomy",
    "Debridement of pancreatic and peripancreatic necrosis",
    "Debulking",
    "Distal subtotal pancreatectomy",
    "Drainage of abscess",
    "Duodenal preserving pancreatic head resection",
    "Endoscopic biopsy",
    "Endoscopic brushings of GIT",
    "Enucleation",
    "Esophageal bypass surgery/jejunostomy only",
    "Exploratory laparotomy",
    "Fine needle aspiration biopsy",
    "Gastric Antrectomy",
    "Hepaticojejunostomy",
    "Ivor Lewis subtotal esophagectomy",
    "Laparotomy (Open and Shut)",
    "Left thoracoabdominal incision",
    "Lobectomy",
    "Mammoplasty",
    "Mastectomy",
    "McKeown esophagectomy",
    "Merendino procedure",
    "Minimally invasive esophagectomy",
    "Pancreaticoduodenectomy",
    "Pancreaticojejunostomy, side-to-side anastomosis",
    "Pneumonectomy",
    "Proximal subtotal gastrectomy",
    "Pylorus-sparing Whipple operation",
    "Radical pancreaticoduodenectomy",
    "Reexcision",
    "Segmentectomy",
    "Sentinal Lymph Node Biopsy",
    "Spleen preserving distal pancreatectomy",
    "Splenectomy",
    "Subtotal pancreatectomy",
    "Thoracotomy (Open & Shut)",
    "Total gastrectomy",
    "Total gastrectomy with extended lymphadenectomy",
    "Total pancreatectomy",
    "Transhiatal esophagectomy",
    "Triple bypass of pancreas",
    "Wedge/localised gastric resection",
    "Wide Local Excision"
]

SURGERY_LOCATION = [
    "Local recurrence",
    "Metastatic",
    "Primary"
]

TUMOUR_FOCALITY = [
    "Cannot be assessed",
    "Multifocal",
    "Not applicable",
    "Unifocal",
    "Unknown"
]

TUMOUR_CLASSIFICATION = [
    "Not applicable",
    "RX",
    "R0",
    "R1",
    "R2",
    "Unknown"
]

MARGIN_TYPES = [
    "Circumferential resection margin",
    "Common bile duct margin",
    "Distal margin",
    "Not applicable",
    "Proximal margin",
    "Unknown"
]

LYMPHOVACULAR_INVASION = [
    "Absent",
    "Both lymphatic and small vessel and venous (large vessel) invasion",
    "Lymphatic and small vessel invasion only",
    "Not applicable",
    "Present",
    "Venous (large vessel) invasion only",
    "Unknown"
]

PERINEURAL_INVASION = [
    "Absent",
    "Cannot be assessed",
    "Not applicable",
    "Present",
    "Unknown"
]

LOST_FOLLOW_UP_REASON = [
    "Completed study",
    "Discharged to palliative care",
    "Lost contact",
    "Not applicable",
    "Unknown",
    "Withdrew from study"
]

DISEASE_STATUS_FOLLOWUP = [
    "Complete remission",
    "Distant progression",
    "Loco-regional progression",
    "No evidence of disease",
    "Partial remission",
    "Progression NOS",
    "Relapse or recurrence",
    "Stable"    
]

RELAPSE_TYPE = [
    "Distant recurrence/metastasis",
    "Local recurrence",
    "Local recurrence and distant metastasis",
    "Progression (liquid tumours)",
    "Biochemical progression"
]

PROGRESSION_STATUS_METHOD = [
    "Imaging (procedure)"
    "Histopathology test (procedure)"
    "Assessment of symptom control (procedure)"
    "Physical examination procedure (procedure)"
    "Tumor marker measurement (procedure)"
    "Laboratory data interpretation (procedure)"
]

MALIGNANCY_LATERALITY =[
    "Bilateral",
    "Left",
    "Midline",
    "Not applicable",
    "Right",
    "Unilateral, Side not specified",
    "Unknown"
]

REGEX_PATTERNS = {
    # ID format
    # Examples: 90234, BLD_donor_89, AML-90
    "ID": r"^[A-Za-z0-9\-\._]{1,64}",
    
    # Date format
    # A date, or partial date (e.g. just year or year + month) as used in
    # human communication. The format is YYYY, YYYY-MM, or YYYY-MM-DD,
    # e.g. 2018, 1973-06, or 1905-08-23. There SHALL be no time zone.
    "DATE": r"^([0-9]([0-9]([0-9][1-9]|[1-9]0)|[1-9]00)|[1-9]000)(-(0[1-9]|1[0-2])(-(0[1-9]|[1-2][0-9]|3[0-1]))?)?",
    
    # ICD-O-3 morphology codes
    # Examples: 8260/3, 9691/36
    "MORPHOLOGY": r"^[8,9]{1}[0-9]{3}/[0,1,2,3,6,9]{1}[1-9]{0,1}$",
    
    # ICD-O-3 topography codes
    # Examples: C50.1, C18
    "TOPOGRAPHY": r"^[C][0-9]{2}(.[0-9]{1})?$",

    # WHO ICD-10 codes
    # Examples: E10, C50.1, I11, M06
    "COMORBIDITY": r"^[A-Z][0-9]{2}(.[0-9]{1,3}[A-Z]{0,1})?$"
}
