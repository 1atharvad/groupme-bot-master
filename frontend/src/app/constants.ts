type BotStatus = 'exists' | 'created' | 'updated';

export interface BotDetails {
  '_id': string,
  'user_name': string,
  'bot_name': string,
  'group_id': string,
  'group_name': string,
  'type': string,
  'bot_status': BotStatus
}