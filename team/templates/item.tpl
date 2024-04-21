<br><br>
    id:         {{it.id}}<br>
    Имя:        {{it.firstname}}<br>
    Фамилия:        {{it.lastname}}<br>
    Возраст:        {{it.age}}<br>
    Опыт:    {{it.experience}}<br>
{% if it.grade or it.grade == "" %}
    Грейд:  {{it.grade}}<br>
{% endif %}

<a href="{{url_for('.edit', id=it.id)}}">Редактировать</a>
<a href="{{url_for('.delete', id=it.id)}}">Удалить</a>

