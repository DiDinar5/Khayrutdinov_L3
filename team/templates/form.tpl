<form method=POST>
    <input type="hidden" name="id" value="{{ form_data.id if form_data.id else 0 }}">
    <div class="field">
        <label>Имя: </label>
        <input type="text" name="firstname" value="{{form_data.firstname}}">
    </div>

    <div class="field">
        <label>Фамилия: </label>
        <input type="text" name="lastname" value="{{form_data.lastname}}">
    </div>

    <div class="field">
        <label>Возраст:</label>
        <input type="text"    name="age"  value="{{form_data.age}}">
    </div>

     <div class="field">
        <label>Опыт:</label>
        <input type="text"    name="experience"  value="{{form_data.experience}}">
    </div>

    {% if not form_data.id or form_data.grade %}
        <div class="field">
            <label>Грейд:</label>
            <input type="text"   name="grade"  value="{{form_data.grade}}">
        </div>
    {% endif %}

    {% if not form_data.id %}
        <input type="submit" formaction="{{ url_for('.add') }}" value="Добавить капитана">
        <input type="submit" formaction="{{ url_for('.add_player') }}" value="Добавить игрока">
    {% else %}
        <input type="submit" formaction="{{ url_for('.confirm_edit') }}" value="Сохранить">
    {% endif %}
</form>