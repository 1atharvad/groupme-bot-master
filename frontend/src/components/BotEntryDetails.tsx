import { Button, FormControl, InputLabel, MenuItem, Select, TextField } from "@mui/material";
import { Delete as DeleteIcon } from '@mui/icons-material';
import { Dispatch, SetStateAction } from "react";
import { BotDetails } from "../constants";

export const BotEntryDetails = ({
  id,
  botEntryState: [botDetails, setBotDetails],
  groupIds,
  existingGroupIds,
  handleDelete
}: {
  id: string,
  botEntryState: [BotDetails, Dispatch<SetStateAction<BotDetails>>],
  groupIds: {[key: string]: string}[],
  existingGroupIds: string[],
  handleDelete: () => void
}) => {
  const handleChange = (e: any) => {
    const { name, value } = e.target;
    const group_details = name === 'group_name'
      ? groupIds.reduce((acc, group) => group.name === value ? {'group_id': group.id, 'group_name': group.name} : acc, {})
      : {[name]: value};

    setBotDetails({...botDetails, ...group_details, 'bot_status': botDetails['bot_status'] === 'exists' ? 'updated' : botDetails['bot_status']});
  };

  return (
    <>
      {groupIds && botDetails && <div className="bot-details">
        <TextField
            id={`${id}-bot-name`}
            name='bot_name'
            label="Bot Name"
            value={botDetails['bot_name']}
            variant='outlined'
            className="input-item"
            onChange={handleChange}
            required/>
        <FormControl className="input-item">
          <InputLabel id={`${id}-group-name-label`}>GroupMe Group Name</InputLabel>
          <Select
              labelId={`${id}-group-name-label`}
              id={`${id}-group-name`}
              name={'group_name'}
              value={botDetails['group_name']}
              onChange={handleChange}
              label='GroupMe Group Name'>
            {groupIds.map(groupDetails => (
              <MenuItem
                  key={groupDetails.id}
                  value={groupDetails.name}
                  disabled={existingGroupIds.includes(groupDetails['id'])}>
                {groupDetails.name}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
        <Button variant='contained' color='error' onClick={handleDelete}>
          <DeleteIcon/>
        </Button>
      </div>}
    </>
  )
}