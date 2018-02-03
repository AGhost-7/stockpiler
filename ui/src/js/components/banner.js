import React from 'react'

export default class Banner extends React.Component {



	render() {
		const {image, other} = this.props
		return (
				<div id='banner' class='row' {...other}>
					<img class='img' src={image} />
				</div>

		)
	}

}

