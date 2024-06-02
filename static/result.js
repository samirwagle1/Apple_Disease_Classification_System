function showEnglish() {
    var enElements = document.getElementsByClassName('en');
    for (var i = 0; i < enElements.length; i++) {
        enElements[i].style.display = 'block';
    }
    var npElements = document.getElementsByClassName('np');
    for (var j = 0; j < npElements.length; j++) {
        npElements[j].style.display = 'none';
    }
}

function showNepali() {
    var enElements = document.getElementsByClassName('en');
    for (var i = 0; i < enElements.length; i++) {
        enElements[i].style.display = 'none';
    }
    var npElements = document.getElementsByClassName('np');
    for (var j = 0; j < npElements.length; j++) {
        npElements[j].style.display = 'block';
    }
}
    