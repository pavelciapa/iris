# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'The number of downloads are properly truncated.'
        self.test_case_id = '99472'
        self.test_suite_id = '1827'
        self.locales = ['en-US']

    def run(self):
        file_to_download = DownloadFiles.SMALL_FILE_10MB

        download_files_list = [DownloadFiles.VERY_LARGE_FILE_1GB, DownloadFiles.EXTRA_LARGE_FILE_512MB,
                               DownloadFiles.MEDIUM_FILE_100MB, DownloadFiles.MEDIUM_FILE_50MB,
                               DownloadFiles.SMALL_FILE_20MB]

        navigate('https://www.thinkbroadband.com/download')

        for file in download_files_list:

            download_file(file, DownloadFiles.OK)
            file_index = download_files_list.index(file)

            if file_index != 0:
                click(DownloadManager.DownloadsPanel.DOWNLOADS_BUTTON)

            expected = exists(DownloadManager.DownloadState.PROGRESS, 10)
            assert_true(self, expected, 'Progress information is displayed.')
            expected = exists(DownloadManager.DownloadState.SPEED_PER_SECOND, 10)
            assert_true(self, expected, 'Speed information is displayed.')

            if file_index == 0:
                expected = exists(DownloadFiles.TOTAL_DOWNLOAD_SIZE_1GB, 10)
                assert_true(self, expected, 'Total size information is displayed for 1 GB file.')

            if file_index == 1:
                expected = exists(DownloadFiles.TOTAL_DOWNLOAD_SIZE_512MB, 10)
                assert_true(self, expected, 'Total size information is displayed for 512 MB file.')

            if file_index == 2:
                expected = exists(DownloadFiles.TOTAL_DOWNLOAD_SIZE_100MB, 10)
                assert_true(self, expected, 'Total size information is displayed for 100 MB file.')

            if file_index == 3:
                expected = exists(DownloadFiles.TOTAL_DOWNLOAD_SIZE_50MB, 10)
                assert_true(self, expected, 'Total size information is displayed for 50 MB file.')

            if file_index == 4:
                expected = exists(DownloadFiles.TOTAL_DOWNLOAD_SIZE_20MB, 10)
                assert_true(self, expected, 'Total size information is displayed for 20 MB file.')

            click(DownloadManager.DownloadsPanel.DOWNLOADS_BUTTON.target_offset(-50, 0))

        download_file(file_to_download, DownloadFiles.OK)

        click(DownloadManager.DownloadsPanel.DOWNLOADS_BUTTON)
        expected = exists(DownloadFiles.DOWNLOAD_FILE_NAME_10MB, 10)
        assert_true(self, expected, '10MB file was downloaded.')

        expected = exists(DownloadManager.DownloadState.COMPLETED, 10)
        assert_true(self, expected, 'Download completed information is displayed.')

        expected = exists(DownloadFiles.DOWNLOAD_FILE_NAME_1GB, 10)
        assert_false(self, expected, '1GB file was removed from the download panel.')

        # Close download panel.
        click(DownloadManager.DownloadsPanel.DOWNLOADS_BUTTON.target_offset(-50, 0))

    def teardown(self):
        # Open the 'Show Downloads' window and cancel all 'in progress' downloads.
        for step in open_clear_recent_history_window_from_library_menu():
            assert_true(self, step.resolution, step.message)

        expected = exists(DownloadManager.DownloadsPanel.DOWNLOAD_CANCEL, 10)
        while expected:
            click(DownloadManager.DownloadsPanel.DOWNLOAD_CANCEL)
            expected = exists(DownloadManager.DownloadsPanel.DOWNLOAD_CANCEL, 10)

        click_window_control('close', 'auxiliary')
