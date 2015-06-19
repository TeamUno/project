angular.module('starter.services', [])

.factory('Places', function() {
  // Might use a resource here that returns a JSON array

  // Some fake testing data
  var places = [{
    id: 0,
    name: 'Ben Sparrow',
    text: 'You on your way?',
    img: 'https://pbs.twimg.com/profile_images/514549811765211136/9SgAuHeY.png'
  }, {
    id: 1,
    name: 'Max Lynx',
    text: 'Hey, it\'s me',
    img: 'https://avatars3.githubusercontent.com/u/11214?v=3&s=460'
  },{
    id: 2,
    name: 'Adam Bradleyson',
    text: 'I should buy a boat',
    img: 'https://pbs.twimg.com/profile_images/479090794058379264/84TKj_qa.jpeg'
  }];

  return {
    all: function() {
      return places;
    },
    remove: function(chat) {
      places.splice(places.indexOf(chat), 1);
    },
    get: function(chatId) {
      for (var i = 0; i < places.length; i++) {
        if (places[i].id === parseInt(chatId)) {
          return places[i];
        }
      }
      return null;
    }
  };
});
