# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.api.helpers.download_manager_utils import download_file, DownloadFiles, downloads_cleanup
from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Clear preview Panel when file is downloading.'
        self.test_case_id = '99822'
        self.test_suite_id = '1827'
        self.locales = ['en-US']

    def run(self):
        download_files_list = [DownloadFiles.VERY_LARGE_FILE_1GB, DownloadFiles.EXTRA_SMALL_FILE_5MB]

        # Download a small file and a large file.
        navigate('https://www.thinkbroadband.com/download')

        for pattern in download_files_list:
            download_file(pattern, DownloadFiles.OK)
            click(DownloadManager.DownloadsPanel.DOWNLOADS_BUTTON.target_offset(-50, 0))

        # Open the Downloads Panel.
        expected = exists(NavBar.DOWNLOADS_BUTTON, 10)
        assert_true(self, expected, '\'Downloads\' button found.')
        click(NavBar.DOWNLOADS_BUTTON)

        # Check that the 5MB download is complete.
        expected = exists(DownloadFiles.DOWNLOADS_PANEL_5MB_COMPLETED, 10)
        assert_true(self, expected, 'The 5MB download is complete.')

        # Open the context menu and select 'Clear Preview Panel'.
        right_click(DownloadFiles.DOWNLOADS_PANEL_5MB_COMPLETED)
        type(text='a')

        # Check that the 1GB download in progress is still displayed.
        expected = exists(DownloadFiles.DOWNLOAD_NAME_1GB, 10)
        assert_true(self, expected, 'The downloaded file name is properly displayed.')

        # Stop the active download.
        expected = exists(DownloadManager.DownloadsPanel.DOWNLOAD_CANCEL, 10)
        assert_true(self, expected, 'The \'X\' button is properly displayed.')
        click(DownloadManager.DownloadsPanel.DOWNLOAD_CANCEL)

        # Cleanup.
        downloads_cleanup('5MB.zip')
