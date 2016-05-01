function getRandomName(elementID) {
    $.ajax({
        url : "/namegen",
        success : function(result){
            var data = result.split("\n");
            var selection = data[Math.floor(Math.random() * data.length - 1)];
            selection += data[Math.floor(Math.random() * data.length)];
            document.getElementById(elementID).value = selection;
        }
    });
}
