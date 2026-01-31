python3 -m nuitka dbcompile.py --mode=standalone \
--run \
--follow-imports \
--company-name=0tanhDSP \
--output-filename=dbcompile \
--include-data-dir=./temp=temp \ 
# --output-folder-name=dbcompilefol\
# --file-description= "testing reading and writing from a local db"\

# cp -r temp/ dbcompile.dist
# --run
# --include-data-dir=src/images \