
function addBadge(parent, content, classHelper){
    var elem = document.createElement('span');
    var attClass = document.createAttribute('class');
    var attDisplay = document.createAttribute('style')
    var title = document.getElementById(parent);
    elem.innerHTML=content;
    attClass.value = 'badge'+ classHelper
    attDisplay.value = '{display: inline;}'
    elem.setAttributeNode(attClass);
    title.setAttributeNode(attDisplay);
    console.log(title,elem);
    $(title).after(elem);
}

function jumboOverwrite(elemID, newContents){
    elem = document.getElementById(elemID);
    elem.innerHTML = newContents;
    elem.id = 'jumbo-error';
}