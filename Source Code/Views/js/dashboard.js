function addFinalLocation(Building){
    var letters = document.getElementById('building')
    for(var i = 0; i < Building.length; i++) {
        var item = document.createElement('li');
        item.append("_");
        letters.appendChild(item);
    }
}