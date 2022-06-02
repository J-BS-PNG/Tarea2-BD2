function add(){
    

    for (let index = 0; index < 10; index++) {
        create(index)
    }
}
function create(value){
    let li = document.createElement("li")

    let button = document.createElement("button")

    button.innerHTML =  value
    li.appendChild(button)
    list.appendChild(li)
}