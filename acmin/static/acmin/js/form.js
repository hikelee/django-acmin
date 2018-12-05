function addChangeEvent(field_group) {
    for (let i in field_group) {
        let fields = field_group[i];
        for (let j = 0; j < fields.length; j++) {
            let attribute = fields[j].attribute;
            $("select[name='" + attribute + "']").change(function () {
                let value = $(this).val();
                for (let k = j + 1; k < fields.length; k++) {
                    let sub_attribute = fields[k].attribute;
                    let selector = "select[name='" + sub_attribute + "']"
                    let select = $(selector);
                    select.html("");
                    if (k == j + 1) {
                        $.getJSON(window.urlPrefix + '/' + fields[k].class + '/', {
                            choices: true,
                            attribute: attribute.substr(sub_attribute.length + 1),
                            value: value
                        }, function (data) {
                            $(data).each(function (i, obj) {
                                let text = obj["title"];
                                let option = "<option value='" + obj.id + "'>" + text + "</option>";
                                console.log(option);
                                $(selector).append(option);
                            });
                        });
                    }
                }

            });
        }
    }
}