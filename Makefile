# Tested with pandoc 3.1.12.1 and lualatex 1.16.0 (TexLive 2023, full
# installation)
paper: Adding-Semantic-Structure-to-PDFs.tex structure.bib
	lualatex -interaction nonstopmode -output-directory=build --shell-escape Adding-Semantic-Structure-to-PDFs.tex

Adding-Semantic-Structure-to-PDFs.tex: Adding-Semantic-Structure-to-PDFs.md
	pandoc -s Adding-Semantic-Structure-to-PDFs.md -C -o Adding-Semantic-Structure-to-PDFs.tex --from markdown+grid_tables+inline_code_attributes --highlight-style=kate

# The following recipe sends the code blocks in the paper to the
# clipboard. The command `pbcopy` is MacOS specific. Linux users
# probably need to change it to something like `xclip`.
examples: Adding-Semantic-Structure-to-PDFs.md
	pandoc --lua-filter extractcode.lua Adding-Semantic-Structure-to-PDFs.md -t markdown -o /dev/null | pbcopy

examples-handout.tex: examples.md
	pandoc -s examples.md -o examples-handout.tex --from markdown+inline_code_attributes --highlight-style=kate

handout: examples-handout.tex
	lualatex -interaction batchmode -output-directory=build --shell-escape examples-handout.tex

clean: 
	rm build/*.aux
	rm build/*.log
	rm build/*.out
	rm build/*.bcf
	rm build/*.xml
