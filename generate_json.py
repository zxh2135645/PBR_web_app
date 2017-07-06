__author__ = 'sf713420'

def get_data(globStr):
    from nipype.utils.filemanip import load_json, save_json
    from glob import glob
    import os
    mse_folders = sorted(glob("/data/henry7/PBR/subjects/{}".format(globStr)))

    #status_file = sorted(glob("/data/henry7/PBR/subjects/mse{}/nii/status.json".format(globStr))) #static is in root
    output_data = []
    for i, foo in enumerate(mse_folders):
        #status = load_json(foo)
        mseid = foo.split('/')[-1]
        print(mseid)
        nii_folders = sorted(glob("/data/henry7/PBR/subjects/{}/nii/status.json".format(mseid)))
        dcm_folders = sorted(glob("/working/henry_temp/PBR_dicoms/{}".format(mseid)))
        #msid = status["t1_files"][0].split('/')[-1].split('-')[0]
        if len(nii_folders) == 0:
            nii = False
        else:
            nii = True
            nii_status = load_json(os.path.join("/data/henry7/PBR/subjects/", mseid, "nii/status.json"))
            dti_count = len(nii_status["dti_files"]) # nested list, why?
            flair_count = len(nii_status["flair_files"])
            gad_count = len(nii_status["gad_files"])
            mt_count = len(nii_status["mt_files"])
            noddi_count = len(nii_status["noddi_files"])

            if "psir_files" in nii_status:
                psir_count = len(nii_status["psir_files"])
            else:
                psir_count = 0
            rsfmri_files = len(nii_status["rsfmri_files"])
            t1_count = len(nii_status["t1_files"])
            t2_count = len(nii_status["t2_files"])

        if len(dcm_folders) == 0:
            dcm = False
        else:
            dcm = True
        output_data.append({"foo": foo,
                            "mse": mseid,
                            #"msid": msid,
                            "nii_folder": nii,
                            "dicom_folder": dcm
                            #"part": None
                            })
        if nii is True:
            output_data[-1]["dti_files"] = dti_count
            output_data[-1]["flair_files"] = flair_count
            output_data[-1]["gad_files"] = gad_count
            output_data[-1]["mt_files"] = mt_count
            output_data[-1]["noddi_files"] = noddi_count
            output_data[-1]["psir_files"] = psir_count
            output_data[-1]["rsfmri_files"] = rsfmri_files
            output_data[-1]["t1_files"] = t1_count
            output_data[-1]["t2_files"] = t2_count
            output_data[-1]["test_mse"] = mseid

    save_json(os.path.join(os.path.realpath('.'), "status.json"), output_data)
    return output_data

if __name__ == '__main__':
    output = get_data('mse12*')
    print(output)