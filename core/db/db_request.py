import asyncpg


class Request:
    def __init__(self, connector: asyncpg.pool.Pool):
        self.connector = connector

    async def get_users_all(self):
        query = f'SELECT * FROM public.users'
        return await self.connector.fetch(query)

    async def get_user(self, telegram_id):
        query = f'SELECT * FROM public.users WHERE telegram_id={telegram_id}'
        return await self.connector.fetchrow(query)

    async def set_user(self, telegram_id, username):
        query = f"INSERT INTO public.users (telegram_id, name, create_at) VALUES ({telegram_id}, '{username}', NOW())"
        await self.connector.fetch(query)

    async def set_expense(self, telegram_id, summ):
        user = await self.get_user(telegram_id)
        query = f"INSERT INTO public.expense (user_id, summ, create_at) VALUES ({user['id']}, '{summ}', NOW())"
        await self.connector.fetch(query)

    async def get_expense(self, telegram_id):
        user_id = await self.get_user(telegram_id)
        query = f"SELECT * FROM public.expense WHERE user_id={user_id['id']}"
        summ = await self.connector.fetch(query)
        all_summ = sum([count['summ'] for count in summ]) if len(summ) > 0 else 0
        return all_summ

    async def get_expense_period(self, telegram_id, period):
        user = await self.get_user(telegram_id)
        query = f"SELECT * FROM public.expense WHERE " \
                f"(create_at >= '{period[0]}' AND create_at <= '{period[1]}') AND user_id={user['id']}"
        summ = await self.connector.fetch(query)
        all_summ = sum([count['summ'] for count in summ]) if len(summ) > 0 else 0
        return all_summ

    async def set_document(self, telegram_id, path):
        user = await self.get_user(telegram_id)
        query = f"INSERT INTO public.files (user_id, path, type, create_at) VALUES " \
                f"({user['id']}, '{path}', 'document', NOW())"
        await self.connector.fetch(query)

    async def set_photo(self, telegram_id, path):
        user = await self.get_user(telegram_id)
        query = f"INSERT INTO public.files (user_id, path, type, create_at) VALUES " \
                f"({user['id']}, '{path}', 'photo', NOW())"
        await self.connector.fetch(query)

    # async def add_data(self, data_user):
    #     query = f'INSERT INTO db_name (column_name) VALUES ({data_user} ON CONFLICT (поле конфликта) ' \
    #             f'DO UPDATE SET column_name={data_user})'
    #     await self.connector.execute(query)
