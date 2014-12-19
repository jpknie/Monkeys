/**
 * Created by janiniem on 13/12/14.
 */

$(function() {
    var friend_button = $("#friend-button");
    var make_friend_button = friend_button.find("#make-friend");
    var unfriend_button = friend_button.find("#unfriend");

    if(make_friend_button.length) {
        friend_button.click(function () {
            var friend_id = make_friend_button.data('friend-id');
            $.ajax(
                {
                    url: 'http://localhost:5000/monkeys/make_friend/' + friend_id,
                    method: 'GET',
                    success: function () {
                        location.href = 'http://localhost:5000/monkeys/profile/' + friend_id
                    }
                }
            );
        });
    }

    else if(unfriend_button.length) {
        friend_button.click(function() {
            var friend_id = unfriend_button.data('friend-id');
            $.ajax(
                {
                    url: 'http://localhost:5000/monkeys/remove_friend/' + friend_id,
                    method: 'GET',
                    success: function () {
                        location.href = 'http://localhost:5000/monkeys/profile/' + friend_id
                    }
                }
            );
        });
    }

});