$('.updateProject').change(function(e){
    var id = e.target.getAttribute('id');
    if(!id){
        return false
    }
    var projectId = e.target.value;
    $.ajax({
        url: "" + window.location.origin + "/Apis/editProject/" + id + "",
        type: "PUT", //send it through get method
        contentType: 'application/json',
        headers:{
           "X-CSRFToken": csrftoken
        },  
        data: JSON.stringify({'projectId':projectId}),
        success: function (response) {
            console.log(response)
        },
        error: function (xhr) {
            alert("Error happenedy");
            //Do Something to handle error
        }
    });
});

$('.updateVersion').change(function(e){
    var name = e.target.getAttribute('name');
    var value = e.target.value;
    var userStoryId = e.target.getAttribute('id');
    $.ajax({
        url: "" + window.location.origin + "/Apis/editUserStoryVersion/" + userStoryId + "",
        type: "PUT", //send it through get method
        contentType: 'application/json',
        headers:{
           "X-CSRFToken": csrftoken
        },  
        data: JSON.stringify({'name':name,'value':value}),
        success: function (response) {
            console.log(response)
        },
        error: function (xhr) {
            alert("Error happenedy");
            //Do Something to handle error
        }
    });
});

function addUserStory(id){
    var userStoryVersionId = id;
    
}