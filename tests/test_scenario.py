import sys
sys.path.extend(['.','..'])
from pdb import set_trace
# see https://click.palletsprojects.com/en/7.x/testing/
from click.testing import CliRunner
from catch.catch import main as catch
from bite.bite import main as bite
from arise.arise import main as arise

# commands in order from SCENARIO.md:
commands = [
  [catch, '-o {pocketmonsters} -k {listofwords} -t {public_forum} -p post'],
  [bite, '-t {public_forum} -p post'],
  [arise, '-o {pocketmonsters} -f {new_synonyms_tfidf}'],
  [bite, '-o {updated-ontology} -t {public_forum} -p post'],
  [catch, '-o {updated-ontology} -k {listofwords} -t {public_forum} -p post']
]

# actual locations (in the jabberwocky-tests submodule) of the
# files in commands
test_files = {
  'pocketmonsters':'tests/jabberwocky-tests/ontology/pocketmonsters.owl',
  'listofwords':'tests/jabberwocky-tests/process/listofwords.txt',
  'updated-ontology':'tests/jabberwocky-tests/process/updated-ontology.owl',
  'public_forum':'tests/jabberwocky-tests/process/public_forum.json',
  'bite_01_tfidf_results':'tests/jabberwocky-tests/process/bite_01_tfidf_results.csv',
  'new_synonyms_tfidf':'tests/jabberwocky-tests/process/new_synonyms_tfidf.csv'
}

out_files = [
  'catch_01_output.txt',
  'catch_01_ontology_dict_class_synonyms.json',
  'updated-ontology.owl',
  'bite_02_tfidf_results.csv',
  'bite_02_ontology_all_terms.txt',
  'catch_02_output.txt'
]

def test_import():
  # everything's cool so far
  pass

def test_scenario():
  runner = CliRunner()
  # test each command run in SCENARIO.md:
  for cmd in commands:
    (script, arg) = cmd
    interp = arg.format(**test_files) # interpolate the actual file paths
    arglist = interp.split(' ') # CliRunner needs a list, not a string
    result = runner.invoke(script,arglist) # Run it!
    assert result.exit_code == 0 # sucessful run
    # additional tests might be
    # examine result.output (a str) in each case, to confirm expected output

