This program is used for scrapping parts in https://rrr.lt/.
You can look for used car parts and save found results.
You can enter maximum price to filter out results. Negative or zero values will not filter results.

How to launch the program:
1. Copy code from GitHub to your PC.
2. Open CMD from src folder.
3. Run pip install selenium command.
4. Run pip install PyYaml command.
5. Run pip install numpy command.
6. Install missing packages if necessary.
7. Use webdriver v101 or v103 depending on your chrome browser version.
8. Start the main.py from src folder.
9. Write name of part you want to search.
10. For testing purpose empty name will look for 'Toyota Distronikas'.
11. Provide more accurate naming for best results.
12. Search results are saved in logs\output_data file.
13. Average price is saved to main.log file.
14. Filtered parts by price are saved in logs\output_data_filtered file.
