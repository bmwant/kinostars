const
  got = require('got'),
  fs = require('fs'),
  mongoose = require('mongoose');



async function downloadImage(starId, path) {
	try {
    const url = `https://st.kp.yandex.net/images/actor_iphone/iphone360_${starId}.jpg`
		const response = await got(url, {followRedirect: true});
    console.log(response.statusCode);
    fs.writeFile(path, response.rawBody, 'binary',  function (err, data) {
      if (err) {
        return console.log(err);
      }
      console.log('Downloaded into ' + path);
    });
	} catch (error) {
    console.log(error);
	}
}

(async () => {
  mongoose.connect('mongodb://localhost/game_db',
  {useNewUrlParser: true,
    useUnifiedTopology: true});
  var schema = new mongoose.Schema({ id: 'Number'});
  var Star = mongoose.model('stars', schema);

  let stars  = await Star.find({});

  stars.forEach(elem => {
    const starId = elem.id;
    const path = `images/${starId}.jpg`
    if (!fs.existsSync(path)) {
      downloadImage(starId, path);
    }
  });

  console.log('Done!');
})();
