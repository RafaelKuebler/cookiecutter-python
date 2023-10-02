# {{ cookiecutter.project_name }}

{{ cookiecutter.project_short_description }}

## Quickstart

{% set is_open_source = cookiecutter.open_source_license != 'Not open source' -%}
{% if is_open_source -%}
## License

Free software: {{ cookiecutter.open_source_license }}
{% endif -%}
