import React from 'react'

export default class Menu extends React.Component {

	constructor(props) {
		super(props)
		this.childrenWithWrapperLi = this.childrenWithWrapperLi.bind(this)
	}

	childrenWithWrapperLi () {
		return React.Children.map(this.props.children, child => {
      return (
        <li>{child}</li> 
			)
		})
	}

	render() {
		const { className, id } = this.props			
		return (
			<ul class={className} id={id}>
				{this.childrenWithWrapperLi()}
			</ul>
		)
	}

}
