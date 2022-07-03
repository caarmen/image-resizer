for project in imageresizer tests
do
  black $project
  PYTHONPATH=. pylint $project
done
