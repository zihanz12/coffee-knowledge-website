$(document).ready(function () {
    // example: https://getbootstrap.com/docs/4.2/components/modal/
    // show modal
// post curd
    $('#task-modal').on('show.bs.modal', function (event) {
        let button = $(event.relatedTarget) // Button that triggered the modal
        let taskID = button.data('source') // Extract info from data-* attributes
        let content = button.data('content') // Extract info from data-* attributes

        let modal = $(this)
        if (taskID === 'New Task') {
            modal.find('.modal-title').text(taskID)
            $('#task-form-display').removeAttr('taskID')
        } else {
            modal.find('.modal-title').text('Edit Post ' + taskID)
            $('#task-form-display').attr('taskID', taskID)
        }

        if (content) {
            modal.find('.form-control').val(content);
        } else {
            modal.find('.form-control').val('');
        }
    })

    $('#CoffeeDrink-modal').on('show.bs.modal', function (event) {
        let button = $(event.relatedTarget) // Button that triggered the modal
        let CoffeeName = button.data('source') // Extract info from data-* attributes
        let content = button.data('content') // Extract info from data-* attributes

        let modal = $(this)
        if (CoffeeName === 'New Drink') {
            modal.find('.modal-title').text(CoffeeName)
            $('#task-form-display').removeAttr('CoffeeName')
        } else {
            modal.find('.modal-title').text('Edit Drink ' + CoffeeName)
            $('#task-form-display').attr('CoffeeName', CoffeeName)
        }

        if (content) {
            modal.find('.form-control').val(content);
        } else {
            modal.find('.form-control').val('');
        }
    })

    $('#button-clear-drink-search').click(function () {
        $.ajax({
            type: 'POST',
            url: '/Fact',
            success: function (res) {
                console.log(res.response)
                location.replace('/Fact');
            },
            error: function () {
                console.log('Error');
            }
        });
    });

    $('#button-search-drink').click(function () {
        let top = parseInt(document.getElementById('selectamount').value)
        if (!Number.isInteger(top)){
            top = 15
        } else {
            top = Math.max(top, 3)
        }
        let Calories = $('#customMaxCal').val()
        let cal_max = $('#customMaxCal').data('content')
        if (Calories >= cal_max) {
            Calories = null
        }
        let selected_cat = $('#selectcategory').val()
        if (selected_cat == "All Category") {
            selected_cat = null
        }
        let obj = {
            'top': top,
            'keyword': $('#keyword').val(),
            'Calories': Calories,
            'selected_cat': selected_cat
        }
        // filter obj whose value = null or ""
        obj = Object.fromEntries(Object.entries(obj).filter(([_, v]) => v != null && v != ""));
        let date = JSON.stringify(obj)
        console.log(date)
        $.ajax({
            type: 'POST',
            url: '/Fact/' + date,
            contentType: 'application/json;charset=UTF-8',
            data: date,
            success: function (res) {
                console.log(res.response)
                location.replace('/Fact/' + date);
            },
            error: function () {
                console.log('Error');
            }
        });
    });

    $('.like_drink').click(function () {
        let like = $(this)
        let liked = like.data('source')
        $.ajax({
            type: 'POST',
            url: (liked ? '/unlike' : '/like') + '/drink/' + like.data('content'),
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
                alert("Error!");
            }
        });
    });

    $('#submit-drink').click(function () {
        let CoffeeName = $('#task-form-display').attr('CoffeeName');
        console.log($('#CoffeeDrink-modal').find('.form-control').val())
        $.ajax({
            type: 'POST',
            url: CoffeeName ? '/edit/drink/' + CoffeeName : '/create_drink',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'Calories': $('#CoffeeDrink-modal').find('.form-control').val()
            }),
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
                document.getElementById('errmess').innerHTML = 'Change Failed, Permission denied';
                document.getElementById('closemodal').onclick = function() {
                    location.reload();
                }
                document.getElementById('closemodal2').onclick = function() {
                    location.reload();
                }
            }
        });
    });

    $('#submit-task').click(function () {
        let tID = $('#task-form-display').attr('taskID');
        console.log($('#task-modal').find('.form-control').val())
        $.ajax({
            type: 'POST',
            url: tID ? '/edit/' + tID : '/create',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'description': $('#task-modal').find('.form-control').val()
            }),
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
                document.getElementById('errmess').innerHTML = 'Change Failed, Permission denied';
                document.getElementById('closemodal').onclick = function() {
                    location.reload();
                }
                document.getElementById('closemodal2').onclick = function() {
                    location.reload();
                }
            }
        });
    });

    $('.remove').click(function () {
        let remove = $(this)
        $.ajax({
            type: 'POST',
            url: '/delete/' + remove.data('source'),
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
                alert("Permission Denied!");
            }
        });
    });

// post search

//added from zihan side:
    function load_data(query) {
        $.ajax({
            url:"/ajaxlivesearch",
            method:"POST",
            data:{query:query},
            success:function(data)
            {
            $('#container').hide();
            $('#AddTask').hide();
            $('#result').html(data);
            $("#result").append(data.htmlresponse);   //appending
            console.log('appending success');
            },
            error: function () {
                console.log('Error');
            }
        });
    }

    $('#search-post').click(function(){
        let content = document.getElementById('query').value;
        if(content != ''){
            load_data(content);
        } else {
            alert("type category name")
            console.log("nothing typed")
        }
    });

 //dirnk search  
    $('#search-drink').click(function () {
        let content = document.getElementById('query').value;
        console.log(content)
        $.ajax({
            type: 'POST',
            url: '/Drinks/searchDrink',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'name': content
            }),
            success: function (res) {
                location.replace("searchDrink");
            },
            error: function () {
                console.log('Error');
            }
        });
    });

    $('#limit-calory').click(function () {  
        let calory_limit = document.getElementById('calories').value;  
        $.ajax({    
            type: 'POST' ,   
            url: '/Drinks/limit-calory',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'limit': calory_limit
            }),  
            success: function (res) {   
                console.log(res.response)
                location.replace("limit-calory"); 

            },  
            error: function () {    
                console.log('Error');   
            }   
        }); 
    });

    $('.remove_drink').click(function () {
        let remove = $(this)
        $.ajax({
            type: 'POST',
            url: '/delete/drink/' + remove.data('source'),
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
                alert("Permission Denied!");
            }
        });
    });

// category search
    function load_flex(query, url) {
        $.ajax({
            url:url,
            method:"POST",
            data:{'query':query},
            success:function(data)
            {
              $('#container').hide();
              $('#AddTask').hide();
              $('#result').html(data);
              $("#result").append(data.htmlresponse);   //appending
              console.log('appending success');
            },
            error: function () {
                console.log('Error');
            }
           });
    }

    $('.search-bean').click(function () {
        console.log('hello')
        let content = $(this).val();
        console.log(content)
        if (content != '') {
            load_flex(content, "/BeanSearch");
        } else {
            alert("Not an option!")
            console.log("Wrong Button");
        }
    });

    $('.search-category').click(function () {
        let content = $(this).val();
        console.log(content)
        if (content != '') {
            load_flex(content, "/CategorySearch");
        } else {
            alert("Not an option!")
            console.log("Wrong Button");
        }
    });


// login, submit, and delete account with trigger
    $('#login-form-submit').click(function () {
        let username = document.getElementById('username-field').value;
        let password = document.getElementById('password-field').value;
        console.log(username)
        console.log(password)
        
        $.ajax({
            url2: '/login',
            type: 'POST',
            url: '/loginbackend',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'username': username, 'password': password
            }),
            success: function (res) {
                    console.log(res)
                    location.replace("../Section");
                },
            error: function (res) {
                console.log(res)
                a = res.responseJSON['response']
                if (a == 'create new') {
                    document.getElementById('login-msg').innerHTML = 'New user? Click <a href="/createuser">here</a > and create an account';
                    console.log('Error');
                } else {
                    document.getElementById('login-msg').innerHTML = 'Wrong Username or Password';
                    console.log('Error');
                }}
            });
    });

    $('#create-form-submit').click(function () {
        let username = document.getElementById('username-enter').value;
        let password = document.getElementById('password-enter').value;
        console.log(username)
        console.log(password)
        $.ajax({
            type: 'POST',
            url: '/createuserbackend',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'username': username, 'password': password
            }),
            success: function (res) {
                document.getElementById('create-msg').innerHTML = 'Account Created!';
                location.replace("/login");
            },
            error: function () {
                console.log('Error');
            }
        });
    });

    $('#delete-account').click(function () {
        $.ajax({
            type: 'POST',
            url: '/deleteacc',
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
                alert("Permission Denied!");
            }
        });
    });



 // code for reference, not useful here.
    $('.state').click(function () {
        let state = $(this)
        let tID = state.data('source')
        let new_state
        if (state.text() === "In Progress") {
            new_state = "Complete"
        } else if (state.text() === "Complete") {
            new_state = "Todo"
        } else if (state.text() === "Todo") {
            new_state = "In Progress"
        }

        $.ajax({
            type: 'POST',
            url: '/edit/' + tID,
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'status': new_state
            }),
            success: function (res) {
                console.log(res)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });
});
