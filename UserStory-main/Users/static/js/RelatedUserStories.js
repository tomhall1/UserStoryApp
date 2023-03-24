$('.relatedUserStory').on('change',function(){
    var epics = Array.from($('.epicInputDetails'));
    console.log(epics)
    epicsValue =[]
    epics.forEach(ep=>{
        epicsValue.push(ep.value)
    })
    var personas = Array.from($('.peronsaInputDetails'));
    personasValue = []
    personas.forEach(ep=>{
        personasValue.push(ep.value)
    })
    relatedUserStory(epicsValue,personasValue);
})
function relatedUserStory(epics,personas){
    $('.relatedUserStory').empty();
    
    var index =0;
    if(epics.length>personas.length){
        index = epics.length;
    }
    else{
        index = personas.length;
    }
    for(var i=0;i<index;i++){
        var epic = "";
        var personaStr = "";
        if(i<epics.length){
            epic = epics[i];
        }
        if(i<personas.length){
            personaStr = personas[i];
        }
        $('.spinner-border').removeClass('d-none')
        $.ajax({
        url: "" + window.location.origin + "/Apis/relatedUserStory",
        type: "get",
        dataType: 'json', //send it through get method
        data: {  
            Persona:personaStr ,
            Epic:epic
        },
        success: function (response) {
            console.log(typeof response);
            data = JSON.parse(response);
            console.log(data[0]);
            if(data){
                var table = $('.d-none')
                table.removeClass('d-none')
                table.addClass('d-block')
            }
            else{
                var table = $('.d-block')
                table.removeClass('d-block')
                table.addClass('d-none')
            }
            data.forEach(element => {

                var iwantTo = $('<td class="align-middle text-center cursor-pointer" id="iWantTO" style="min-width: 16.5rem;">'+ element['iWantTO'] +'</td>')
                var soThat = $('<td class="align-middle text-center cursor-pointer" id="soThat" style="min-width: 16.5rem;">'+ element['soThat'] +'</td>')
                var epic = $('<td class="align-middle text-center cursor-pointer" id="epic" style="min-width: 16.5rem;">'+ element['epic'] +'</td>')
                var priority = $('<td class="align-middle text-center cursor-pointer" id="priority">'+ element['priority'] +'</td>')
                var devTask = $('<td class="align-middle text-center cursor-pointer" id="devTask" style="min-width: 31.5rem ;">'+ element['devTask'].join() +'</td>')
                var RAIDS = $('<td class="align-middle text-center cursor-pointer" id="RAIDS" style="min-width: 31.5rem ;">'+ element['RAIDS'].join() +'</td>')
                var persona = $('<td class="align-middle text-center cursor-pointer" id="persona" style="min-width: 16.5rem;">'+ element['persona'].join() +'</td>')
                var row = $('<tr id='+ element['id'] +' onclick=selectUserStory(event,this)></tr>')
                row.append($('<td></td>')).append(persona).append(epic).append(iwantTo).append(soThat).append(devTask).append(RAIDS);
                $('.relatedUserStory').append(row);
                var table = $('.relatedUserStory').parent('table');
                table =   table.parent()
                table.css("cssText", "max-height: 15rem !important;overflow-y: auto;overflow-x: hidden;width: " + $('#mainTable').width() + "px !important;");
                $('.spinner-border').addClass('d-none')
                $('.spinner-border').removeClass('d-block')
            });
        },
        error: function (xhr) {
            $('.spinner-border').addClass('d-none')
            $('.spinner-border').removeClass('d-block')
            //Do Something to handle error
        }
    });
    }
    $('.spinner-border').addClass('d-none')
    $('.spinner-border').removeClass('d-block')
}

async function selectUserStory(e){
    var element = $(e.target);
    var userStoryId = $('.currentInput[name="IWantTO"]').closest('tr').attr('id');
    if(e.target.tagName == "TD")
    {
        element = $(e.target.parentNode);
    }
    var children = element.children();
    $.ajax({
        url: "" + window.location.origin + "/Apis/addSelectedUserStory/" + userStoryId + "",
        type: "PUT", //send it through get method
        contentType: 'application/json',
        headers:{
           "X-CSRFToken": csrftoken
        },  
        data: JSON.stringify({'id':element.attr('id')}),
        success: function (response) {
            data = JSON.parse(response);
            for(var i =0;i<children.length;i++){
                switch (children[i].id) {
                    case 'iWantTO':
                        $('.currentInput[name="IWantTO"]').val(children[i].textContent);
                        $('.currentInput[name="IWantTO"]').val(function (i, val) {
                                return val + "\n";
                            });
                            if (!$('.currentInput[name="IWantTO"]').val()) {
                                e.target.style.height = 'auto';
                            }
                            else {
                                $('.currentInput[name="IWantTO"]').css("cssText", "height: " + $('.currentInput[name="IWantTO"]').prop("scrollHeight") + "px !important;");
                        }
                        break;
                    case 'soThat':
                        $('.currentInput[name="SoThat"]').val(children[i].textContent);
                        $('.currentInput[name="SoThat"]').val(function (i, val) {
                                return val + "\n";
                            });
                            if (!$('.currentInput[name="SoThat"]').val()) {
                                e.target.style.height = 'auto';
                            }
                            else {
                                $('.currentInput[name="SoThat"]').css("cssText", "height: " + $('.currentInput[name="SoThat"]').prop("scrollHeight") + "px !important;");
                        }
                        break;
                    case 'epic':
                        $('.currentInput[name="Epic"]').val(children[i].textContent);
                        $('.currentInput[name="Epic"]').val(function (i, val) {
                                return val + "\n";
                            });
                            if (!$('.currentInput[name="Epic"]').val()) {
                                e.target.style.height = 'auto';
                            }
                            else {
                                $('.currentInput[name="Epic"]').css("cssText", "height: " + $('.currentInput[name="Epic"]').prop("scrollHeight") + "px !important;");
                        }
                        break;
                    case 'priority':
                        //$('.currentInput[name="Epic"]').val(children[i].textContent);
                        break;
                    case 'persona':
                        $('.currentInput[name="Persona"]').val(data['persona'][0]['name']);
                        $('.currentInput[name="Persona"]').attr('data-id',data['persona'][0]['id']);
                        $('.currentInput[name="Persona"]').val(function (i, val) {
                                return val + "\n";
                            });
                            if (!$('.currentInput[name="Persona"]').val()) {
                                e.target.style.height = 'auto';
                            }
                            else {
                                $('.currentInput[name="Persona"]').css("cssText", "height: " + $('.currentInput[name="Persona"]').prop("scrollHeight") + "px !important;");
                        }
                        $('.PersonDiv').empty();
                        for(var x =1;x<data['persona'].length;x++){
                            var form = $('<div class=" form-group row"></div>')
                            $('<i class="col-2 m-auto text-danger fa fa-times" onclick="remove(this)" style="display: flex;justify-content: center;align-items: center;cursor: pointer;"</i>').prependTo(form);
                            $('<div class="col-10 m-0 p-0"><textarea type="text" class="form-control bg-gray"  name="Persona" id="exampleInputEmail1" aria-describedby="emailHelp" placeholder="Persona" data-id="'+ data['persona'][x]['id'] +'">' + data['persona'][x]['name'] + '</textarea></div>').prependTo(form);
                            form.prependTo($('.PersonDiv'));
                        }
                        
                        break;
                    case 'RAIDS':
                        $('.currentInput[name="RAIDS"]').val(data['RAIDS'][0]['name']);
                        $('.currentInput[name="RAIDS"]').attr('data-id',data['RAIDS'][0]['id']);
                        $('.currentInput[name="RAIDS"]').val(function (i, val) {
                                return val + "\n";
                            });
                            if (!$('.currentInput[name="RAIDS"]').val()) {
                                e.target.style.height = 'auto';
                            }
                            else {
                                $('.currentInput[name="RAIDS"]').css("cssText", "height: " + $('.currentInput[name="RAIDS"]').prop("scrollHeight") + "px !important;");
                        }
                        $('.RAIDSDiv').empty();
                        for(var x =1;x<data['RAIDS'].length;x++){
                            var form = $('<div class="w-100 form-group row twiceWidth"></div>')
                            $('<i class="col-2 m-auto text-danger fa fa-times" onclick="remove(this)" style="display: flex;justify-content: center;align-items: center;cursor: pointer;"</i>').prependTo(form);
                            var textArea = $('<textarea type="text" class="form-control" style="height: 38px !important;" name="RAIDS" id="exampleInputEmail1" aria-describedby="emailHelp" placeholder="RAIDS" data-id="'+ data['RAIDS'][x]['id'] +'">' + data['RAIDS'][x]['name'] + '</textarea>')
                            textArea.val(function (i, val) {
                                return val + "\n";
                            });
                            textArea = resizeTextArea(textArea);
                            textArea.prependTo($('<div class="col-10 m-0 p-0"></div>').prependTo(form));
                            form.prependTo($('.RAIDSDiv'));
                        }
                        break;
                    case 'devTask':
                        $('.currentInput[name="Dev"]').val(data['devTask'][0]['name']);
                        $('.currentInput[name="Dev"]').attr('data-id',data['devTask'][0]['id']);
                        $('.currentInput[name="Dev"]').val(function (i, val) {
                                return val + "\n";
                            });
                            if (!$('.currentInput[name="Dev"]').val()) {
                                e.target.style.height = 'auto';
                            }
                            else {
                                $('.currentInput[name="Dev"]').css("cssText", "height: " + $('.currentInput[name="Dev"]').prop("scrollHeight") + "px !important;");
                        }
                        $('.DKDiv').empty();
                        for(var x =1;x<data['devTask'].length;x++){
                            var form = $('<div class="form-group row twiceWidth"></div>')
                            $('<i class="col-2 m-auto text-danger fa fa-times" onclick="remove(this)" style="display: flex;justify-content: center;align-items: center;cursor: pointer;"</i>').prependTo(form);
                            var textArea = $('<textarea type="text" style="height:auto !important" class="form-control bg-gray" name="Dev" id="exampleInputEmail1" aria-describedby="emailHelp" placeholder="Persona" data-id="'+ data['devTask'][x]['id'] +'"></textarea>')
                            textArea.val(data['devTask'][x]['name']);
                            textArea.val(function (i, val) {
                                return val + "\n";
                            });
                            textArea = resizeTextArea(textArea);
                            textArea.prependTo($('<div class="col-10 m-0 p-0"></div>').prependTo(form));
                            form.prependTo($('.DKDiv'));
                        }
                }
            }

        },
        error: function (xhr) {
            alert("Error happenedy");
            //Do Something to handle error
        }
    });
}

function resizeTextArea(element){
    var originalValue = $('.currentInput[name="Dev"]').val();
    $('.currentInput[name="Dev"]').val(element.val());
    var scrollHeight = $('.currentInput[name="Dev"]').prop("scrollHeight")
    $('.currentInput[name="Dev"]').val(originalValue);
    element.css("cssText", "height: " + scrollHeight + "px !important;");
    return element
}
