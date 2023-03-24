var csrftoken = $("[name=csrfmiddlewaretoken]").val();
$('.addIndustry').on('click',function(e){
    var industry =  $('#industry').val();
    
    if(industry){
    $.ajax({
        url: "" + window.location.origin + "/Apis/addIndustry",
        type: "Post", //send it through get method
        contentType: 'application/json',
        headers:{
           "X-CSRFToken": csrftoken
        },  
        data: JSON.stringify({'name':industry}),
        success: function (response) {
            console.log(response);
            $(`<button type="button" class="multiselect-option dropdown-item" title="`+ response['name'] +`,"><span class="form-check">
            <input class="form-check-input" type="checkbox" value="`+response['id']+`" id="multiselect_vjjommr0br_0_0">
            <label class="form-check-label" for="multiselect_vjjommr0br_0_0">`+response['name']+`,</label></span>
            </button>`).appendTo($('.multiselect-container:first'))
            $('<option value="'+ response['id'] +'" data-multiselectid="multiselect_vjjommr0br_0_0">'+response['name']+',</option>').appendTo($('.industry'))
        },
        error: function (xhr) {
            alert("Error happenedy");
            //Do Something to handle error
        }
    });
   }
});