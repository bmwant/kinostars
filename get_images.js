const
  got = require('got'),
  fs = require('fs');



(async () => {
	try {
		const response = await got(
      'https://st.kp.yandex.net/images/actor_iphone/iphone360_38702.jpg',
      {followRedirect: true}
    );
      console.log(response.statusCode);
      console.log(response.content);
		// console.log(response.body);
    //=> '<!doctype html> ...'
    fs.writeFile('images/test.jpg', response.rawBody, 'binary',  function (err, data) {
      if (err) {
        return console.log(err);
      }
      console.log(data);
    });
	} catch (error) {
    console.log(error);
	}
})();
