for project in imageresizer
do
  black $project
  PYTHONPATH=. pylint $project
done
