import React from 'react'
import PropTypes from 'prop-types'
import { Link } from 'react-router-dom'

export default class MenuItem extends React.Component {

	static propTypes = {
		href: PropTypes.string,
		className: PropTypes.string,
		children: PropTypes.node
	}

	constructor(props) {
		super(props)
	}

	render() {
		const { href, children, className, ...props } = this.props
		return (
			<Link to={href} className={className} {...props}>
				{children}
			</Link>
		)
	}

}
