var csrftoken = $("[name=csrfmiddlewaretoken]").val();
$('.updatePersona').change(function(e){
    console.log(this)
    var personaId = e.target.getAttribute('data-id');
    var persona = e.target.value;
    var userStoryId = $(this).closest('tr').attr('id');
    console.log(window.location.origin);
    if(personaId){
        $.ajax({
        url: "" + window.location.origin + "/Apis/editPersona/" + personaId + "",
        type: "PUT", //send it through get method
        contentType: 'application/json',
        headers:{
           "X-CSRFToken": csrftoken
        },  
        data: JSON.stringify({'persona':persona}),
        success: function (response) {
            console.log(response)
        },
        error: function (xhr) {
            alert("Error happenedy");
            //Do Something to handle error
        }
    });
    }
});

function removeField(name,id){
    $.ajax({
        url: "" + window.location.origin + "/Apis/RemoveField",
        type: "PUT", //send it through get method
        contentType: 'application/json',
        headers:{
           "X-CSRFToken": csrftoken
        },  
        data: JSON.stringify({'name':name,'id':id}),
        success: function (response) {
            console.log(response)
        },
        error: function (xhr) {
            alert("Error happenedy");
            //Do Something to handle error
        }
    });
}

function addPersona(e){
    var userStoryId = $(e.target).closest('tr').attr('id');
    var persona = e.target.value;
    var personaId = e.target.getAttribute('data-id');
    if(personaId>0){
        $.ajax({
        url: "" + window.location.origin + "/Apis/editPersona/" + personaId + "",
        type: "PUT", //send it through get method
        contentType: 'application/json',
        headers:{
           "X-CSRFToken": csrftoken
        },  
        data: JSON.stringify({'persona':persona}),
        success: function (response) {
            $(e.target).attr('data-id', response['id']);
            var epics = Array.from($('.epicInputDetails'));
            console.log(epics)
            epicsValue =[]
            epics.forEach(ep=>{
                epicsValue.push(ep.value)
            })
            var personas = Array.from($('textarea[name="Persona"]'));
            personasValue = []
            personas.forEach(ep=>{
                personasValue.push(ep.value)
            })
            relatedUserStory(epicsValue,personasValue);
            console.log(response)
        },
        error: function (xhr) {
            alert("Error happenedy");
            //Do Something to handle error
        }
    });
    }
    else{
        $.ajax({
        url: "" + window.location.origin + "/Apis/addPersona/" + userStoryId + "",
        type: "POST", //send it through get method
        contentType: 'application/json',
        headers:{
           "X-CSRFToken": csrftoken
        },  
        data: JSON.stringify({'persona':persona}),
        success: function (response) {
            $(e.target).attr('data-id', response['id']);
            var epics = Array.from($('.epicInputDetails'));
            console.log(epics)
            epicsValue =[]
            epics.forEach(ep=>{
                epicsValue.push(ep.value)
            })
            var personas = Array.from($('textarea[name="Persona"]'));
            personasValue = []
            personas.forEach(ep=>{
                personasValue.push(ep.value)
            })
            relatedUserStory(epicsValue,personasValue);
            console.log(response)
        },
        error: function (xhr) {
            alert("Error happenedy");
            //Do Something to handle error
        }
    });
    }
}

$('.updateDevTask').change(function(e){
    var devTaskId = e.target.getAttribute('data-id');
    var devTask = e.target.value;
    var userStoryId = $(this).closest('tr').attr('id');
    if(devTaskId){
        $.ajax({
        url: "" + window.location.origin + "/Apis/editDevTask/" + devTaskId + "",
        type: "PUT", //send it through get method
        contentType: 'application/json',
        headers:{
           "X-CSRFToken": csrftoken
        },  
        data: JSON.stringify({'devTask':devTask}),
        success: function (response) {
            console.log(response)
        },
        error: function (xhr) {
            alert("Error happenedy");
            //Do Something to handle error
        }
    });
    }
});

function addDevTask(e){
    var userStoryId = $(e.target).closest('tr').attr('id');
    var devTaskId = e.target.getAttribute('data-id');
    var devTask = e.target.value;
    if(devTaskId>0){
        $.ajax({
        url: "" + window.location.origin + "/Apis/editDevTask/" + devTaskId + "",
        type: "PUT", //send it through get method
        contentType: 'application/json',
        headers:{
           "X-CSRFToken": csrftoken
        },  
        data: JSON.stringify({'devTask':devTask}),
        success: function (response) {
            console.log(response)
        },
        error: function (xhr) {
            alert("Error happenedy");
            //Do Something to handle error
        }
    });
    }
    else{
         $.ajax({
        url: "" + window.location.origin + "/Apis/addDevTask/" + userStoryId + "",
        type: "POST", //send it through get method
        contentType: 'application/json',
        headers:{
           "X-CSRFToken": csrftoken
        },  
        data: JSON.stringify({'devTask':devTask}),
        success: function (response) {
            $(e.target).attr('data-id', response['id']);
            console.log(response)
        },
        error: function (xhr) {
            alert("Error happenedy");
            //Do Something to handle error
        }
    });
    }
    
}


$('.updateRaids').change(function(e){
    var raidsId = e.target.getAttribute('data-id');
    var raids = e.target.value;
    var userStoryId = $(this).closest('tr').attr('id');
    if(raidsId>0){
        $.ajax({
        url: "" + window.location.origin + "/Apis/editRaids/" + raidsId + "",
        type: "PUT", //send it through get method
        contentType: 'application/json',
        headers:{
           "X-CSRFToken": csrftoken
        },  
        data: JSON.stringify({'raids':raids}),
        success: function (response) {
            console.log(response)
        },
        error: function (xhr) {
            alert("Error happenedy");
            //Do Something to handle error
        }
    });
    }
});

function addRaids(e){
    var userStoryId = $(e.target).closest('tr').attr('id');
    var raidsId = e.target.getAttribute('data-id');
    var raids = e.target.value;
    if(raidsId>0){
        $.ajax({
        url: "" + window.location.origin + "/Apis/editRaids/" + raidsId + "",
        type: "PUT", //send it through get method
        contentType: 'application/json',
        headers:{
           "X-CSRFToken": csrftoken
        },  
        data: JSON.stringify({'raids':raids}),
        success: function (response) {
            console.log(response)
        },
        error: function (xhr) {
            alert("Error happenedy");
            //Do Something to handle error
        }
    });
    }
    else{
         $.ajax({
        url: "" + window.location.origin + "/Apis/addRaids/" + userStoryId + "",
        type: "POST", //send it through get method
        contentType: 'application/json',
        headers:{
           "X-CSRFToken": csrftoken
        },  
        data: JSON.stringify({'raids':raids}),
        success: function (response) {
            $(e.target).attr('data-id', response['id']);
            console.log(response)
        },
        error: function (xhr) {
            alert("Error happenedy");
            //Do Something to handle error
        }
    });
    }
}

$('.updateUserStory').change(function(e){
    var name = e.target.getAttribute('data-name');
    var value = e.target.value;
    var userStoryId = $(this).closest('tr').attr('id');
    $.ajax({
        url: "" + window.location.origin + "/Apis/editUserStory/" + userStoryId + "",
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

$('.updateEstimate').change(function(e){
    UpdateTotalEstimates();
    var estimateId = e.target.getAttribute('data-id');
    var estimate = e.target.value;
    $.ajax({
        url: "" + window.location.origin + "/Apis/editEstimate/" + estimateId + "",
        type: "PUT", //send it through get method
        contentType: 'application/json',
        headers:{
           "X-CSRFToken": csrftoken
        },  
        data: JSON.stringify({'estimate':estimate}),
        success: function (response) {
            UpdateTotalEstimates();
        },
        error: function (xhr) {
            alert("Error happenedy");
            //Do Something to handle error
        }
    });
});



function addEstimate(e){
    var estimate = e.target.value;
    var userStoryId = $(e.target).closest('tr').attr('id');
    var element = $(e.target);
    var id = e.target.id
    if(e.target.getAttribute('data-id')>0){
        var estimateId = e.target.getAttribute('data-id');
        $.ajax({
        url: "" + window.location.origin + "/Apis/editEstimate/" + estimateId + "",
        type: "PUT", //send it through get method
        contentType: 'application/json',
        headers:{
           "X-CSRFToken": csrftoken
        },  
        data: JSON.stringify({'estimate':estimate}),
        success: function (response) {
            UpdateTotalEstimates();
        },
        error: function (xhr) {
            alert("Error happenedy");
            //Do Something to handle error
        }
    });
    }
    else{
        $.ajax({
        url: "" + window.location.origin + "/Apis/addEstimate/" + userStoryId + "",
        type: "Post", //send it through get method
        contentType: 'application/json',
        headers:{
           "X-CSRFToken": csrftoken
        },  
        data: JSON.stringify({'estimate':estimate,'id':id}),
        success: function (response) {
            element.attr('data-id',response['id']);
            UpdateTotalEstimates();
        },
        error: function (xhr) {
            alert("Error happenedy");
            //Do Something to handle error
        }
    });
    }
}
$('#AddPlatform').on('click',function AddPlatfom(e){
   var platform =  $('#platformName').val();
   $('#platformName').val("");
   if(platform){
    $.ajax({
        url: "" + window.location.origin + "/Apis/addPlatform",
        type: "Post", //send it through get method
        contentType: 'application/json',
        headers:{
           "X-CSRFToken": csrftoken
        },  
        data: JSON.stringify({'platform':platform}),
        success: function (response) {
            console.log(response);
            $(`<button type="button" class="multiselect-option dropdown-item" title="`+ response['name'] +`,"><span class="form-check">
            <input class="form-check-input" type="checkbox" value="`+response['id']+`" id="multiselect_vjjommr0br_0_0">
            <label class="form-check-label" for="multiselect_vjjommr0br_0_0">`+response['name']+`,</label></span>
            </button>`).appendTo($('.multiselect-container:first'))
            $('<option value="'+ response['id'] +'" data-multiselectid="multiselect_vjjommr0br_0_0">'+response['name']+',</option>').appendTo($('.platform'))
        },
        error: function (xhr) {
            alert("Error happenedy");
            //Do Something to handle error
        }
    });
   }
});



function UpdateTotalEstimates() {
    var platform = $(".platform").val();
    
    var table = $('.sumEstimatesTable');
    table.empty();
    for(var i = 0 ;i< platform.length;i++){
        var name = $('.platform option[value="'+ platform[i] +'"]');
        var allEstimates = $("input[id^="+ platform[i] +"]");
        var total = 0
        for(var x = 0;x<allEstimates.length;x++){
            total = total + parseInt(allEstimates[x].value);
        }
        console.log(name);
        console.log(total);
        table.append($('<tr><td>'+ name.text() +'</td><td>'+ total +'</td></tr>'));
    }
}
function selectPriority(e){
    finalResult = [];
    var value = $(e.target).val();
    for(var i=0;i<value.length;i++){
        var elements = Array.from($('input[name="Priority"]'));
        elements.forEach(element=>{
            if($(element).val()==value[i]){

                var inputs = Array.from($(element).closest("td").nextAll());
                inputs.forEach(input=>{
                    var id =  $(input).children().children().attr('id');
                    var text= $('.platform option[value="'+ id +'"]').text();
                    var total =parseInt($(input).children().children().val());
                    objIndex = finalResult.findIndex((obj => obj.id == id))
                    if(objIndex!=-1){
                        finalResult[objIndex]['total'] = finalResult[objIndex]['total'] + total; 
                    }else{
                        finalResult.push({'id':id,'name':text,'total':total})
                    }
                })
            }
        });
    }
    console.log(finalResult);
    var table = $('.sumEstimatesTable');
    table.empty();
    finalResult.forEach(final=>{
        table.append($('<tr><td>'+ final['name'] +'</td><td>'+ final['total'] +'</td></tr>'));
    });
}