# Download PROCAR files from Nomad

curl "http://nomad-lab.eu/prod/rae/api/raw/query?upload_id=EIDyjluDQ3eZnt-gI7Fc4Q&file_pattern=PROCAR.gz" --output nomad.zip

# Extract atom wave function projection by procar_parser.py
python procar_parser.py

# You can run the commands on fidis using scripts in bash_scripts
submit the bash script in this folder by ``` sbatch bash_scripts/run_<python_program>.sh ```