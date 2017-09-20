import sys
import zipfile

lab = sys.argv[1]

zip = zipfile.ZipFile('downloaded/{}/archive/submissions.zip'.format(lab))

print("last_name,id,no,file_id")
for l in zip.namelist():
    print(",".join(l.split("_")))
