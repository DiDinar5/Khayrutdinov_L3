{% extends "base.tpl" %}

{% block title %}Player{% endblock %}

{% block content %}

    {% for title, bp in bps %}
        <a href="{{loop.index}}">{{title}}</a><br>
    {% endfor %}

{% endblock %}
