import React from 'react'
import { List } from 'semantic-ui-react'

const ListComponent = (props) => (
  <List >
    {
      Object.keys(props.items).map(function(key) {
        return <List.Item >{props.items[key]}</List.Item>
      }.bind(this))
    }
</List>
)

export default ListComponent