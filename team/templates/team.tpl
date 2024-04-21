{% extends "base.tpl" %}

{% block title %}Team{% endblock %}

{% block content %}

    {% include "form.tpl" ignore missing %}

    {% if items %}
        <a href="{{url_for('.clear')}}">Очистить</a><br>
    {% endif %}

    {% for it in items %}
        {% include "item.tpl" ignore missing %}
    {% else %}
        <label>
            База пустая
        </label>
    {% endfor %}

{% endblock %}