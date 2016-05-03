function getRandomName(elementID) { // TODO: request namegen data once, instead every time.
    $.ajax({
        url : "/namegen",
        success : function(result){
            var data = result.split("\n");
            var selection = data[Math.floor(Math.random() * data.length)];
            selection += data[Math.floor(Math.random() * data.length)];
            document.getElementById(elementID).value = selection;
        }
    });
}
