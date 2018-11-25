import React from 'react';
import PropTypes from 'prop-types';

class Delayed extends React.Component {

    constructor(props) {
        super(props);
        this.state = {hidden : true};
    }

    componentDidMount() {
        setTimeout(() => {
            this.setState({hidden: false},() => {this.refs.loading_elem.style.display='none'});
        }, this.props.waitBeforeShow);
    }

    render() {
        return (
            <div class="ui inverted segment">
            <div ref="loading_elem" className="ui inverted placeholder">
                    <div className="image header">
                    <div className="line"></div>
                    <div className="line"></div>
                    </div>
            </div>
        
        {this.state.hidden ? '' : this.props.children}
        
        </div>
        );
    }
}

Delayed.propTypes = {
  waitBeforeShow: PropTypes.number.isRequired
};

export default Delayed;