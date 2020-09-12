const admin = require('firebase-admin');

var serviceAccount = require('./kinostars-firebase-admin.json');

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  databaseURL: "https://kinostars-96deb.firebaseio.com"
});

var MongoClient = require('mongodb').MongoClient;
var url = 'mongodb://localhost:27017/';
const remoteDb = admin.firestore();

MongoClient.connect(url, function(err, db) {
  if (err) throw err;
  var dbo = db.db('game_db');
  dbo.collection('stars').find().toArray(function(err, res) {
    if (err) throw err;
    res.forEach((elem) => {
      let category = 'default';
      if (elem.category === 'Актрисы') {
        category = 'actress'
      } else if (elem.category === 'Актёры') {
        category = 'actor'
      } else if (elem.category === 'Режиссеры') {
        category = 'director'
      }
      remoteDb.collection('stars').add({
        name: elem.name,
        nameOrig: elem.orig_name,
        starId: parseInt(elem.id),
        category: category,
      });
    });
    db.close();
  });
});
