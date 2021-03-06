from pathlib import Path
from pprint import pprint
import matplotlib.pyplot as plt
import pydicom
from pydicom import dcmread
from pydicom.data import get_testdata_file
import os
import PySide6

qtdir = os.path.dirname(PySide6.__file__)
plugin_path = os.path.join(qtdir, "plugins", "platforms")
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path

#path = os.path("./rawdata/1.2.840.113619.2.353.2807.8104482.21577.1643185400.362")
ds = dcmread("./rawdata/1.2.840.113619.2.353.2807.8104482.21577.1643185400.362/")
root_dir = Path(ds.filename).resolve().parent
print(f"Root directory: {root_dir}\n")

# Iterate through the PATIENT records
for patient in ds.patient_records:
    print(
        f"PATIENT: PatientID={patient.PatientID}, "
        f"PatientName={patient.PatientName}"
    )

    # Find all the STUDY records for the patient
    studies = [
        ii for ii in patient.children if ii.DirectoryRecordType == "STUDY"
    ]
    for study in studies:
        descr = study.StudyDescription or "(no value available)"
        print(
            f"{'  ' * 1}STUDY: StudyID={study.StudyID}, "
            f"StudyDate={study.StudyDate}, StudyDescription={descr}"
        )

        # Find all the SERIES records in the study
        all_series = [
            ii for ii in study.children if ii.DirectoryRecordType == "SERIES"
        ]
        for series in all_series:
            # Find all the IMAGE records in the series
            images = [
                ii for ii in series.children
                if ii.DirectoryRecordType == "IMAGE"
            ]
            plural = ('', 's')[len(images) > 1]

            descr = getattr(
                series, "SeriesDescription", "(no value available)"
            )
            print(
                f"{'  ' * 2}SERIES: SeriesNumber={series.SeriesNumber}, "
                f"Modality={series.Modality}, SeriesDescription={descr} - "
                f"{len(images)} SOP Instance{plural}"
            )

            # Get the absolute file path to each instance
            #   Each IMAGE contains a relative file path to the root directory
            elems = [ii["ReferencedFileID"] for ii in images]
            # Make sure the relative file path is always a list of str
            paths = [[ee.value] if ee.VM == 1 else ee.value for ee in elems]
            paths = [Path(*p) for p in paths]

            # List the instance file paths
            for p in paths:
                print(f"{'  ' * 3}IMAGE: Path={os.fspath(p)}")

                # Optionally read the corresponding SOP Instance
                # instance = dcmread(Path(root_dir) / p)
                # print(instance.PatientName)