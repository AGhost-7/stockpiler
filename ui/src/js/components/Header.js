import React, { Component } from 'react'
import Navigation from './header/Navigation'
class Header extends Component {
	constructor() {
		super()
		this.state = {
			title: 'StockPiler'
		}
	}

	render() {
		return (
			<header className="header">
				<Navigation title={this.state.title} />
			</header>
		)
	}
}

export default Header
