'use client';

import { Box, Button, Divider, Fab } from "@mui/material";
import AddIcon from '@mui/icons-material/Add';
import { FormEvent, useEffect, useState } from "react";
import { BotEntryDetails } from "@/components/BotEntryDetails";
import { BotDetails } from "@/app/constants";
import { useAuthRedirect } from '@/hooks/useAuthRedirect';
import '@/scss/admin.scss';

export default function Admin() {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL;
  const [storedUsername, setStoredUsername] = useState<string | null>(null);
  const [groupIds, setGroupIds] = useState<{[key: string]: string}[]>([]);
  const [groupDetails, setGroupDetails] = useState<{[key: string]: BotDetails[]}>({});
  const [existingGroupIds, setExistingGroupIds] = useState<string[]>([]);
  useAuthRedirect();

  const defaultBotDetails: BotDetails = {
    '_id': '',
    'user_name': storedUsername ? storedUsername : '',
    'bot_name': '',
    'group_id': '',
    'group_name': '',
    'type': '',
    'bot_status': 'created'
  }

  useEffect(() => {
    if (typeof window !== 'undefined') {
      const username = sessionStorage.getItem("username");
      setStoredUsername(username);
    }
  }, []);

  useEffect(() => {
    if (storedUsername) {
      fetch(`${apiUrl}api/get-group-ids/${storedUsername}`, {
        method: "GET"
      })
        .then(response => {
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          return response.json();
        })
        .then(fetchedData => {
          if (fetchedData['group_ids']) setGroupIds(fetchedData['group_ids']);
        })
        .catch((error) => console.error("Error fetching client ID:", error));
      
      fetch(`${apiUrl}api/get-bot-groups/${storedUsername}`, {
        method: "GET"
      })
        .then(response => {
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          return response.json()
        })
        .then(fetchedData => {
          if (fetchedData) setGroupDetails(fetchedData);
        })
        .catch((error) => console.error("Error fetching client ID:", error));
    }
  }, [storedUsername, apiUrl]);

  useEffect(() => {
    setExistingGroupIds(Object.values(groupDetails).flat().map((group: BotDetails) => group.group_id));
  }, [groupDetails]);

  const addNewEntry = (_type: string) => {
    setGroupDetails(previousDetails => {
      defaultBotDetails.type = _type;
      return {...previousDetails, [_type]: [...previousDetails[_type], defaultBotDetails]};
    });
  }

  const submitBtn = (_type: string) => {
    groupDetails[_type].map((group, index) => {
      if (group['bot_status'] === 'created') {
        group['bot_status'] = 'exists';

        fetch(`${apiUrl}api/set-bot-groups`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(group)
        })
          .then(response => {
            if (!response.ok) {
              throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
          })
          .then(fetchedData => {
            const groupDetails = fetchedData as BotDetails;

            setGroupDetails(previousDetails => {
              const groups = Object.fromEntries(Object.entries(previousDetails[groupDetails.type]));
              groups[index] = groupDetails;
              return {...previousDetails, [groupDetails.type]: Object.values(groups)};
            });
          })
          .catch((error) => console.error("Error creating group:", error));
      } else if (group['bot_status'] === 'updated') {
        group['bot_status'] = 'exists';

        fetch(`${apiUrl}api/update-bot-groups/${group['_id']}`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(group)
        })
          .then(response => {
            if (!response.ok) {
              throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
          })
          .then(fetchedData => {
            const groupDetails = fetchedData as BotDetails;

            setGroupDetails(previousDetails => {
              const groups = Object.fromEntries(Object.entries(previousDetails[groupDetails.type]));
              groups[index] = groupDetails;
              return {...previousDetails, [groupDetails.type]: Object.values(groups)};
            });
          })
          .catch((error) => console.error("Error updating group:", error));
      }
    });
  }

  const deleteEntry = (group: BotDetails) => {
    if (group.bot_status !== 'created') {
      fetch(`${apiUrl}api/delete-bot-group/${group['_id']}`, {
        method: "DELETE"
      })
        .then(response => {
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
        })
        .catch((error) => console.error("Error updating group:", error));
    }
  }

  return (
    <>
      {groupDetails && <div className="bot-details-container">
        <Box
            component="form"
            className="admin-details"
            onSubmit={(event: FormEvent) => {
              event.preventDefault();
              submitBtn('admin_group');
            }}>
          <div className="title-grid">
            <h2 className="title">Admin Group</h2>
            {groupDetails && groupDetails.admin_group && groupDetails.admin_group.length > 0 &&
              <Button type="submit" variant='contained' color='primary' className="submit-btn">
                Save Group Details
              </Button>
            }
          </div>
          {groupDetails.admin_group && groupDetails.admin_group.length > 0 ? (
            <BotEntryDetails 
                id='admin'
                existingGroupIds={existingGroupIds}
                botEntryState={[groupDetails.admin_group[0], (updatedValue) => {
                  setGroupDetails(previousDetails => {
                    return {...previousDetails, ['admin_group']: [updatedValue as BotDetails]};
                  });
                }]}
                groupIds={groupIds}
                handleDelete={() => {
                  if (window.confirm("Do you want to delete the bot from GroupMe?")) {
                    deleteEntry(groupDetails.admin_group[0]);
                    setGroupDetails(previousDetails => {
                      return {...previousDetails, ['admin_group']: []};
                    });
                  }
                }}/>
          ) : (
            <button className="create-btn" onClick={() => addNewEntry('admin_group')}>
              Create an Admin Bot
            </button>
          )}
        </Box>
        <Box
            component="form"
            className="target-details"
            onSubmit={(event: FormEvent) => {
              event.preventDefault();
              submitBtn('target_groups');
            }}>
          <div className="title-grid">
            <h2 className="title">Target Groups</h2>
            {groupDetails && groupDetails.target_groups && groupDetails.target_groups.length > 0 &&
              <Button type="submit" variant='contained' color='primary' className="submit-btn">
                Save Group Details
              </Button>
            }
          </div>
          {groupDetails.target_groups && groupDetails.target_groups.length > 0 ? (
            <>
              {groupDetails.target_groups.map((group, index) => (
                <BotEntryDetails
                    key={index}
                    id={`target-${index}`}
                    existingGroupIds={existingGroupIds}
                    botEntryState={[group, (updatedValue) => {
                      setGroupDetails(previousDetails => {
                        const targetGroups = Object.fromEntries(Object.entries(previousDetails['target_groups']));
                        targetGroups[index] = updatedValue as BotDetails;
                        return {...previousDetails, ['target_groups']: Object.values(targetGroups)};
                      });
                    }]}
                    groupIds={groupIds}
                    handleDelete={() => {
                      if (window.confirm("Do you want to delete the bot from GroupMe?")) {
                        deleteEntry(group);
                        setGroupDetails(previousDetails => {
                          return {...previousDetails, ['target_groups']: previousDetails['target_groups'].filter((_, _index) => index !== _index)};
                        });
                      }
                    }}/>
              ))}
              <Divider className='add-new-btn'>
                <Fab color="primary" size="medium" aria-label="add" title='Add new group' onClick={() => addNewEntry('target_groups')}>
                  <AddIcon/>
                </Fab>
              </Divider>
            </>
          ) : (
            <button className="create-btn" onClick={() => addNewEntry('target_groups')}>
              Create a Target Bot
            </button>
          )}
        </Box>
      </div>}
    </>
  )
}