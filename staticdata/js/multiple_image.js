let imgForm = document.querySelectorAll(".img-form")
let container = document.querySelector("#form-container")
let addButton = document.querySelector("#add-img-button")
let totalForms = document.querySelector("#id_form-TOTAL_FORMS")

let formNum = imgForm.length - 1
addButton.addEventListener('click', addForm)

function addForm(e) {
    e.preventDefault()

    if (formNum < 2) {
        let newForm = imgForm[0].cloneNode(true)
        let formRegex = RegExp(`form-(\\d){1}-`, 'g')

        formNum++
        newForm.innerHTML = newForm.innerHTML.replace(formRegex, `form-${formNum}-`)
        container.insertBefore(newForm, addButton)

        totalForms.setAttribute('value', `${formNum + 1}`)
    }
    else if (formNum === 2) {
        var error = document.getElementById("images-error");
        if (!error) {
            let p = document.createElement('p');
            p.id = "images-error"
            p.innerHTML = 'Максимум 3 изображения';
            container.insertBefore(p, addButton)
        }
    }
}