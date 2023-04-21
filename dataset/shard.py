"""
Turns directory like
abap.jsonl            coldfusion.jsonl                gentoo-eclass.jsonl          jupyter-notebook.jsonl          nimrod.jsonl                          qml.jsonl                 svg.jsonl
actionscript.jsonl    common-lisp.jsonl               gettext-catalog.jsonl        kit.jsonl                       ninja.jsonl                           r.jsonl                   swift.jsonl
ada.jsonl             coq.jsonl                       glsl.jsonl                   kotlin.jsonl                    nit.jsonl                             racket.jsonl              systemverilog.jsonl
agda.jsonl            creole.jsonl                    gnuplot.jsonl                krl.jsonl                       nix.jsonl                             ragel-in-ruby-host.jsonl  tcl.jsonl
ags-script.jsonl      crystal.jsonl                   go.jsonl                     labview.jsonl                   nsis.jsonl                            raml.jsonl                tcsh.jsonl
alloy.jsonl           csound.jsonl                    golo.jsonl                   lasso.jsonl                     nu.jsonl                              rdoc.jsonl                tea.jsonl
antlr.jsonl           css.jsonl                       gosu.jsonl                   latte.jsonl                     numpy.jsonl                           realbasic.jsonl           tex.jsonl
apacheconf.jsonl      csv.jsonl                       grammatical-framework.jsonl  lean.jsonl                      objective-c++.jsonl                   rebol.jsonl               text.jsonl
api-blueprint.jsonl   cucumber.jsonl                  graphql.jsonl                less.jsonl                      objective-j.jsonl                     red.jsonl                 textile.jsonl
apl.jsonl             cuda.jsonl                      graphviz-dot.jsonl           lex.jsonl                       ocaml.jsonl                           redcode.jsonl             thrift.jsonl

into directory with one dir for each language and 500MB shards of its jsonl within that dir.
"""
import os
import json

# Define the maximum shard size in bytes
max_shard_size = 500 * 1024 * 1024

# Iterate over the files in the current directory
for filename in sorted(os.listdir('.')):
    if not filename.endswith('.jsonl'):
        continue
    print(filename)

    # Rename the file
    new_filename = filename.replace('_new', '')
    os.rename(filename, new_filename)

    # Create the directory and move the file into it
    dirname = os.path.splitext(new_filename)[0]
    os.makedirs(dirname, exist_ok=True)
    os.rename(new_filename, os.path.join(dirname, new_filename))

    # Shard the file
    shard_num = 1
    shard_size = 0
    with open(os.path.join(dirname, new_filename)) as f_in:
        shard_lines = []
        for line in f_in:
            line_size = len(line.encode('utf-8'))
            if shard_size + line_size > max_shard_size:
                # Write the current shard to a file
                shard_filename = os.path.join(dirname, f"{new_filename.replace('.jsonl', '')}-{shard_num:04d}.jsonl")
                with open(shard_filename, 'w') as f_out:
                    f_out.writelines(shard_lines)
                shard_num += 1
                shard_size = 0
                shard_lines = []
            shard_lines.append(line)
            shard_size += line_size

        # Write the last shard to a file
        shard_filename = os.path.join(dirname, f"{new_filename.replace('.jsonl', '')}-{shard_num:04d}.jsonl")
        with open(shard_filename, 'w') as f_out:
            f_out.writelines(shard_lines)
    os.remove(os.path.join(dirname, new_filename))
