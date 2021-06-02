


function get_data_from_modal() {

    name = $("#node_name").val()
    description = $("#node_description").val()
    
    data = {
    "name": name,
    "description": description }
    return data
}


function posted_data() {
    // Add a loading indicator here if time permits.
}


function add_node() {
    // Add a NEW data source to the list.

    modal_data = get_data_from_modal()
    
    if (modal_data['name'] == '') {
        bootbox.alert({message:"A Name is required, a description is optional",
        backdrop: true })
        return
    }


    $.post("/add_node",modal_data, posted_data())
    

    .done(function() {
        bootbox.alert({message:"Table Added",
        backdrop: true })
        })

    
    .fail(function(xhr, textStatus, error) {
        alert(error)
    })
}


function delete_node(node_id){
    // Delete a datasource
    var element = document.getElementById(node_id);
    element.classList.add("table-danger");
  
  
  
    bootbox.confirm('Are you sure you want to delete '.concat(node_id).concat('?'), function(result){ 
                        if (result) {
                                data = {"index": node_id}                                
                                $.post("/delete_node",data, posted_data() )    
                                                        
                                .done(function() {   
                                    $( "#".concat(node_id) ).remove()
                                    })
                                                
                                .fail(function(xhr, textStatus, error) {
                                    alert(error)
                                })                                   
                        }
                        
                        if (result!== true) {
                            var element = document.getElementById(node_id);
                            element.classList.remove("table-danger");
  
                        }
                        return
                    })
}


function add_node_button(){
    // Adding a node button modifies the Modal
    $('#node_name').prop('readonly', false);
    search_bar_text = $("#search_bar").val()
    set_modal_data("Add A New Table", search_bar_text, "")

}

function edit_node_button(index, description){
    // Editing a node button modifies the modal to lock in the name.
    $('#node_name').prop('readonly', true);
    set_modal_data("Modify Existing Table", index, description)

}

function set_modal_data(header_text, index, description) {
    $("#modal-title").text(header_text)
    $("#node_name").val(index)
    $("#node_description").val(description)
    }
    
function clear_search_bar_text(){
    document.getElementById("search_bar").value = ""
}


function reload_relationship_results(index, kind) {
    information = {
        "kind": kind,
        "index": index
    }
    
    $.get('/get_relationships', information , 
        function(data, status) {
        console.log(data)
            content_box = $('#relationship_content')
            content_box.replaceAll( data )
        }    
    ).fail(function(xhr, textStatus, error) {
            alert(error)
        }) 

}

