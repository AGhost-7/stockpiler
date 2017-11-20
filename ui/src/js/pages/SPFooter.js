import React, { Component } from 'react'
import { Footer } from 'react-materialize'


class SPFooter extends Component {
	render() {
		return (
			<Footer copyrights='&copy; 2015 Copyright StockPiler' className='footer'>
				<h5 className='white-text'>Footer Content</h5>
				<p className='grey-text text-lighten-4'>You can use rows and columns here to organize your footer content.</p>
			</Footer>
		)
	}
}

export default SPFooter
