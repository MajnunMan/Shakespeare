var json = JSON.parse(localStorage.getItem("content"));
console.log(json)
// testing
/*json = {
  data: {
    category: "food",
    text: "Want to try out our new chocolate fudge ice cream reciepe? Check it out at goo.gl/i3Rk9"
  },
  result:{
    score: 30,
    tweets: [
      {
        name: "Chris Turnbull",
        username: "@chefchris86",
        dateTime: "20h",
        text: "New week new lunch menu Rhubarb and whisky tart, rhubarb sorbet.",
        hashtags: "#food #chef #dessert #pastrychef",
        comments: 94,
        retweets: 185,
        likes: 203,
        image: "../public/img3.jpg"
      },
      {
        name: "Food Truck Fridays",
        username: "@lovefoodtruckfridays",
        dateTime: "2h",
        text: "Think you have the best food truck in the country? We are on the lookout for more food trucks for Food Truck Fridays from across the land. If you have what it takes, send an email with info and pics of your truck to welove@foodtruckfridays.co.za.",
        hashtags: "#welovefoodtruckfridays #food",
        comments: 80,
        retweets: 110,
        likes: 199,
        image: "../public/img1.jpg"
      },
      {
        name: "Food Pictures",
        username: "@foodpictures666",
        dateTime: "12h",
        text: "Think you have the best food truck in the country? We are on the lookout for more food trucks for Food Truck Fridays from across the land. If you have what it takes, send an email with info and pics of your truck to welove@foodtruckfridays.co.za.",
        hashtags: "#welovefoodtruckfridays #food",
        comments: 80,
        retweets: 110,
        likes: 199,
        image: "../public/img2.jpg"
      },
      {
        name: "The Whitby Guide",
        username: "@thewhitbyguide",
        dateTime: "1h",
        text: "What’s your favorite Whitby restaurant? Here are 16 of our favourite restaurants in Whitby - bit.ly/1esFDHf #whitby #Food #Foodies",
        hashtags: "#whitby #Food #Foodies",
        comments: 5,
        retweets: 300,
        likes: 555,
        image: "../public/img4.jpg"
      },
      {
        name: "Chris Turnball",
        username: "@chefchris86",
        dateTime: "20h",
        text: "New week new lunch menu Rhubarb and whisky tart, rhubarb sorbet. #food #chef #dessert #pastrychef",
        hashtags: "#food #chef #dessert #pastrychef",
        comments: 40,
        retweets: 50,
        likes: 90,
        image: "../public/img5.jpg"
      },
      {
        name: "Food Truck Fridays",
        username: "@lovefoodtruckfridays",
        dateTime: "2h",
        text: "Think you have the best food truck in the country? We are on the lookout for more food trucks for Food Truck Fridays from across the land. If you have what it takes, send an email with info and pics of your truck to welove@foodtruckfridays.co.za.",
        hashtags: "#welovefoodtruckfridays #food",
        comments: 80,
        retweets: 110,
        likes: 199,
        image: "../public/img6.jpg"
      },
      {
        name: "Chris Turnbull",
        username: "@chefchris86",
        dateTime: "20h",
        text: "New week new lunch menu Rhubarb and whisky tart, rhubarb sorbet.",
        hashtags: "#food #chef #dessert #pastrychef",
        comments: 94,
        retweets: 185,
        likes: 203,
        image: "../public/img7.jpg"
      },
      {
        name: "Food Truck Fridays",
        username: "@lovefoodtruckfridays",
        dateTime: "2h",
        text: "Think you have the best food truck in the country? We are on the lookout for more food trucks for Food Truck Fridays from across the land. If you have what it takes, send an email with info and pics of your truck to welove@foodtruckfridays.co.za.",
        hashtags: "#welovefoodtruckfridays #food",
        comments: 80,
        retweets: 110,
        likes: 199,
        image: "../public/img8.jpg"
      },
      {
        name: "Food Pictures",
        username: "@foodpictures666",
        dateTime: "12h",
        text: "Think you have the best food truck in the country? We are on the lookout for more food trucks for Food Truck Fridays from across the land. If you have what it takes, send an email with info and pics of your truck to welove@foodtruckfridays.co.za.",
        hashtags: "#welovefoodtruckfridays #food",
        comments: 80,
        retweets: 110,
        likes: 199,
        image: "../public/img9.jpg"
      },
      {
        name: "The Whitby Guide",
        username: "@thewhitbyguide",
        dateTime: "1h",
        text: "What’s your favorite Whitby restaurant? Here are 16 of our favourite restaurants in Whitby - bit.ly/1esFDHf #whitby #Food #Foodies",
        hashtags: "#whitby #Food #Foodies",
        comments: 5,
        retweets: 300,
        likes: 555,
        image: "../public/img10.jpg"
      }
    ]
  }
}

json.result.score = JSON.parse(localStorage.getItem("content")).result.score*/
debugger
console.log(json)

function addImgs(obj){
	let i = 0;
	obj.result.tweets = obj.result.tweets.map(function(tweet){
		i++;
		tweet.image = "../public/img"+i+".jpg";
		return (tweet);	
	})
	return obj;
}

function calc_passed(date1){
	
	var date2 = new Date();

	var diff = date2.getTime() - date1.getTime();
	
	var years = Math.floor(diff / (1000 * 60 * 60 * 24 * 365));
	diff -=  years * (1000 * 60 * 60 * 24 * 365);

	var days = Math.floor(diff / (1000 * 60 * 60 * 24));
	diff -=  days * (1000 * 60 * 60 * 24);

	var hours = Math.floor(diff / (1000 * 60 * 60));
	diff -= hours * (1000 * 60 * 60);

	var mins = Math.floor(diff / (1000 * 60));
	diff -= mins * (1000 * 60);

	var seconds = Math.floor(diff / (1000));
	diff -= seconds * (1000);

	return years + " years, " + days + " days, " + hours + " hours";
}

// var ProgressBar = require('progressbar.js');

$( document ).ready(function() {

  var bar = new window.ProgressBar.Line('#progress-bar', {
    easing: 'easeInOut',
    color: '#d82763',
    strokeWidth: 3,
    trailWidth: 1
  });
  bar.animate(json.result.score/100);

  $("#tw-name-js").html("Shakespeare");
  $("#tw-username-js").html("@Shakespeare");
  $("#tw-date-time-js").html("Now");
  $("#final-score-js").html(json.result.score);
  $("#tw-text-js").html(json.data.text);
  $("#tw-hashtags-js").html("#"+json.data.category);
	json = addImgs(json);
	console.log(json);
  // other tweete
  json.result.tweets.forEach(function(tweet){
    $( "#simmilar-tweets-js" ).append(
      '<div class="tw-body row">'+
        '<img src="'+ tweet.image +'" alt="default user picture" class="img-circle col-xs-2">' +
        '<div class="col-xs-10 tw-content">' +
          '<div class="tw-header row">' +
            '<h4 class="tw-name">'+ tweet.name +'</h4> <span class="tw-username">'+ tweet.username +'</span> <span>&#183;</span> <span class="tw-date-time">'+ calc_passed(new Date(tweet.dateTime)) +'</span>' +
          '</div>' +
          '<div class="tw-text row">'+ tweet.text +'</div>' +
          /*'<div class="tw-hashtags row">'+ tweet.hashtags +'</div>' +*/
          '<div class="tw-popularity row">' +
            /*'<i class="glyphicon glyphicon-comment"></i>' +
            '<span class="tw-comments">'+ tweet.comments +'</span>' +*/
            '<i class="glyphicon glyphicon-retweet"></i>' +
            '<span class="tw-retweets">'+ tweet.retweets +'</span>' +
            /*'<i class="glyphicon glyphicon-heart-empty"></i>' +
            '<span class="tw-likes">'+ tweet.likes +'</span>' +*/
          '</div>' +
        '</div>' +
      '</div>'
    );
  })
});
