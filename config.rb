require 'find'

http_path = '/'
css_dir = (environment == :development) ? 'simplelivepoll/static/styles-dev' : 'simplelivepoll/static/styles'
sass_dir = 'simplelivepoll/sass'
images_dir = 'simplelivepoll/static/images'
javascripts_dir = 'simplelivepoll/static/scripts'
http_generated_images_path = '../images'

output_style = :compressed
line_comments = (environment == :development) ? true : false

preferred_syntax = :sass

python_path = `python -c "import sys; sys.stdout.write(':'.join(sys.path))"`
python_path = python_path.split(':').find_all {|path| FileTest.exists? path}

Find.find(*python_path) do |filepath|
  name = File.basename(filepath)
  if name.index('.')
    Find.prune
  elsif FileTest.directory? filepath and ( name == 'sass')
    add_import_path filepath
  end
end
