/* global process */

import * as React from 'react';
import { Socket } from './Socket';
import TwitterLogin from "react-twitter-login";
import { CoolButton } from "./CoolButton";
import './css/button.css';

export function TwitterButton() 
{
	function authHandler(err, data)
	{
		console.log(err, data);
		Socket.emit('login_oauth_twitter', {
		  'err': err,
		  'data': data
		});
	}
 
  return (
	<TwitterLogin
		className='twitter-btn'
		authCallback={authHandler}
      	consumerKey={process.env.TWITTER_CONSUMER_KEY}
	  	consumerSecret={process.env.TWITTER_CONSUMER_SECRET} 
	/>
  );
}

// render={renderProps => (
// 	<AwesomeButton type="anchor" onClick={renderProps.onClick}>LOGIN IN WITH FACEBOOK</AwesomeButton>
// )}