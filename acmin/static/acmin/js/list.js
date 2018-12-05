function updateBoolAttribute(class_name, id, element) {
    let url = window.urlPrefix + "/" + class_name + "/" + id + "/";
    let data = {attribute: element.name, value: element.checked, partial: true};
    $.getJSON(url, data, function (result) {
        console.log(result)
    });
    console.log(url, data)
}