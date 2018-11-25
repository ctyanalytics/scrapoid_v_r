import React, { Component } from 'react'
import { Button,  Icon,  Menu, Segment, Sidebar } from 'semantic-ui-react'
import ScrapoidContainer from './ScrapoidContainer.js';

export default class DashBoardScrapoidComponent extends Component {
  state = { visible: false }

  handleHideClick = () => this.setState({ visible: false })
  handleShowClick = () => this.setState({ visible: true })
  handleSidebarHide = () => this.setState({ visible: false })

  render() {
    const { visible } = this.state

    return (
      <div>
        <Button.Group>
          <Button size="mini" disabled={visible} onClick={this.handleShowClick}>
            Scrapoid Settings ON
          </Button>
          <Button.Or size="mini"/>
          <Button size="mini" disabled={!visible} onClick={this.handleHideClick}>
          Scrapoid Settings OFF
          </Button>
        </Button.Group>

        <Sidebar.Pushable as={Segment}>
          <Sidebar
            as={Menu}
            animation='scale down'
            icon='labeled'
            inverted
            onHide={this.handleSidebarHide}
            vertical
            visible={visible}
            width='thin'
            direction="right"
          >
            <Menu.Item as='a'>
              <Icon name='home' />
              Home
            </Menu.Item>
            <Menu.Item as='a'>
              <Icon name='redo' />
              Reset
            </Menu.Item>
          
          </Sidebar>

          <Sidebar.Pusher dimmed={visible} >
            
            
              <ScrapoidContainer></ScrapoidContainer>
           
          </Sidebar.Pusher>

          
        </Sidebar.Pushable>

         
      </div>
    )
  }
}